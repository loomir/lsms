from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.auth import (
    TokenResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.auth_service import auth_service
from app.repositories.user_repository import get_user_by_email, get_user_by_id
from app.core.dependencies import get_current_user
from app.core.security import verify_password, hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("/test")
def auth_test():
    return {"message": "Auth router working"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_obj = auth_service.register(db, user)
        return user_obj
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password

    user = auth_service.authenticate(db, email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token, refresh_token = auth_service.create_tokens(db, user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = auth_service.refresh(db, payload.refresh_token)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    ok = auth_service.logout(db, payload.refresh_token)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or already logged out")
    return None


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(payload: ChangePasswordRequest, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    ok = auth_service.change_password(db, current_user, payload.current_password, payload.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    return {"message": "Password changed successfully"}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = auth_service.forgot_password(db, payload.email)
    if not token:
        # do not reveal whether email exists in production
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"reset_token": token}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    ok = auth_service.reset_password(db, payload.email, payload.token, payload.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token or email")
    return {"message": "Password reset successful"}


@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    return current_user
