from sqlalchemy.orm import Session

from app.repositories.user_profile_repository import (
    create_user_profile,
    get_user_profiles,
    get_user_profile_by_email,
)
from app.schemas.user_profile import UserProfileCreate


class UserProfileService:

    def create_user_profile(self, db: Session, user_profile: UserProfileCreate):
        existing = get_user_profile_by_email(db, user_profile.email)
        if existing:
            raise ValueError("Client email already exists")

        return create_user_profile(db, user_profile)

    def get_user_profiles(self, db: Session):
        return get_user_profiles(db)

    def create_client(self, db: Session, user_profile: UserProfileCreate):
        return self.create_user_profile(db, user_profile)

    def get_clients(self, db: Session):
        return self.get_user_profiles(db)


user_profile_service = UserProfileService()