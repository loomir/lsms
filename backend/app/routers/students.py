from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_profile import UserProfileCreate
from app.services.user_profile_service import user_profile_service

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/test")
def students_test():
    return {"message": "Students router working"}


@router.post("/")
def create_student(
    user_profile: UserProfileCreate,
    db: Session = Depends(get_db)
):
    try:
        return user_profile_service.create_user_profile(db, user_profile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_students(
    db: Session = Depends(get_db)
):
    return user_profile_service.get_user_profiles(db)