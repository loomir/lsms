from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.core.security import hash_password
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    hashed = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed,
        role=user.role,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.execute(statement).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    return db.execute(statement).scalar_one_or_none()


def update_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_reset_password_token(db: Session, user: User, token: str, expires_at: datetime) -> User:
    user.reset_password_token = token
    user.reset_password_expires_at = expires_at
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def clear_reset_password_token(db: Session, user: User) -> None:
    user.reset_password_token = None
    user.reset_password_expires_at = None
    db.add(user)
    db.commit()


def get_user_by_reset_token(db: Session, token: str) -> User | None:
    statement = select(User).where(User.reset_password_token == token)
    return db.execute(statement).scalar_one_or_none()


def update_user_password(db: Session, user: User, hashed_password: str) -> User:
    user.password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
