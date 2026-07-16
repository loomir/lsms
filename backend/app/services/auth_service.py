from datetime import datetime, timedelta
from typing import Tuple
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_password_reset_token,
    decode_token,
    verify_password,
    hash_password,
)
from app.repositories.user_repository import get_user_by_email, get_user_by_id, create_user as repo_create_user, update_user
from app.repositories.refresh_token_repository import (
    create_refresh_token as repo_create_refresh_token,
    get_refresh_token as repo_get_refresh_token,
    revoke_refresh_token as repo_revoke_refresh_token,
)
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register(db: Session, payload: UserCreate):
        existing = get_user_by_email(db, payload.email)
        if existing:
            raise ValueError("Email already registered")
        user = repo_create_user(db, payload)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        user = get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def create_tokens(db: Session, user) -> Tuple[str, str]:
        # sub should be user id as str
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        # store refresh token in DB with expiry
        try:
            payload = decode_token(refresh_token)
            exp = payload.get("exp")
            if isinstance(exp, int):
                expires_at = datetime.utcfromtimestamp(exp)
            else:
                # fallback to config
                expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        except JWTError:
            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        repo_create_refresh_token(db, user.id, refresh_token, expires_at)
        return access_token, refresh_token

    @staticmethod
    def refresh(db: Session, refresh_token_str: str) -> Tuple[str, str]:
        # validate token exists and not revoked
        rt = repo_get_refresh_token(db, refresh_token_str)
        if not rt or rt.revoked or rt.expires_at < datetime.utcnow():
            return None, None
        try:
            payload = decode_token(refresh_token_str)
        except JWTError:
            return None, None
        if payload.get("type") != "refresh":
            return None, None
        user = get_user_by_id(db, int(payload.get("sub")))
        if not user:
            return None, None
        # Optionally revoke old token and issue a rotated refresh token
        repo_revoke_refresh_token(db, refresh_token_str)
        access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        try:
            new_payload = decode_token(new_refresh_token)
            exp = new_payload.get("exp")
            expires_at = datetime.utcfromtimestamp(exp) if isinstance(exp, int) else datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        except JWTError:
            expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        repo_create_refresh_token(db, user.id, new_refresh_token, expires_at)
        return access_token, new_refresh_token

    @staticmethod
    def logout(db: Session, refresh_token_str: str) -> bool:
        rt = repo_get_refresh_token(db, refresh_token_str)
        if not rt:
            return False
        repo_revoke_refresh_token(db, refresh_token_str)
        return True

    @staticmethod
    def change_password(db: Session, user, current_password: str, new_password: str) -> bool:
        if not verify_password(current_password, user.password):
            return False
        hashed = hash_password(new_password)
        update_user(db, user)
        user.password = hashed
        db.add(user)
        db.commit()
        db.refresh(user)
        return True

    @staticmethod
    def forgot_password(db: Session, email: str) -> str | None:
        user = get_user_by_email(db, email)
        if not user:
            return None
        token = None
        try:
            token = create_password_reset_token(email)
        except Exception:
            # fallback: create a signed jwt with create_refresh_token (not ideal)
            token = create_refresh_token({"sub": str(user.id)})
        # figure expires_at
        try:
            payload = decode_token(token)
            exp = payload.get("exp")
            expires_at = datetime.utcfromtimestamp(exp) if isinstance(exp, int) else datetime.utcnow() + timedelta(minutes=settings.RESET_PASSWORD_EXPIRE_MINUTES)
        except JWTError:
            expires_at = datetime.utcnow() + timedelta(minutes=settings.RESET_PASSWORD_EXPIRE_MINUTES)
        # save token to user
        from app.repositories.user_repository import save_reset_password_token
        save_reset_password_token(db, user, token, expires_at)
        # In production send email; here return token for testing
        return token

    @staticmethod
    def reset_password(db: Session, email: str, token: str, new_password: str) -> bool:
        # verify token belongs to user and is not expired
        from app.repositories.user_repository import get_user_by_reset_token, clear_reset_password_token, update_user_password
        user = get_user_by_reset_token(db, token)
        if not user or user.email != email:
            return False
        # validate token content
        try:
            payload = decode_token(token)
        except JWTError:
            return False
        if payload.get("type") != "reset":
            return False
        # set new password
        hashed = hash_password(new_password)
        update_user_password(db, user, hashed)
        clear_reset_password_token(db, user)
        return True


auth_service = AuthService()