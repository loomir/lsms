from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_profile import UserProfileCreate, UserProfileResponse
from app.services.user_profile_service import user_profile_service

router = APIRouter(
    prefix="/user-profiles",
    tags=["User Profiles"],
)


@router.post("/", response_model=UserProfileResponse, status_code=201)
def create_user_profile(
    user_profile: UserProfileCreate,
    db: Session = Depends(get_db),
):
    try:
        return user_profile_service.create_user_profile(db, user_profile)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[UserProfileResponse])
def get_user_profiles(db: Session = Depends(get_db)):
    return user_profile_service.get_user_profiles(db)


@router.get("/{user_profile_id}", response_model=UserProfileResponse)
def get_user_profile_by_id(user_profile_id: int, db: Session = Depends(get_db)):
    user_profile = user_profile_service.get_user_profile_by_id(db, user_profile_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return user_profile
