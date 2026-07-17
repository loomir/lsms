from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.user_profile import UserProfile
from app.models.academic_info import AcademicInfo
from app.schemas.user_profile import UserProfileCreate


def create_user_profile(db: Session, user_profile: UserProfileCreate) -> UserProfile:
    db_user_profile = UserProfile(
        name=user_profile.name,
        email=user_profile.email,
        dob=user_profile.dob,
        gender=user_profile.gender,
        grade=user_profile.grade,
        phone=user_profile.phone,
        address=user_profile.address,
        status=user_profile.status,
    )

    try:
        db.add(db_user_profile)
        db.flush()

        student = Student(
            id=db_user_profile.id,
            name=db_user_profile.name,
            email=db_user_profile.email,
            dob=db_user_profile.dob,
            gender=db_user_profile.gender,
            grade=db_user_profile.grade,
            phone=db_user_profile.phone,
            address=db_user_profile.address,
            status=db_user_profile.status,
        )
        db.add(student)
        db.flush()

        existing_academic = db.query(AcademicInfo).filter(AcademicInfo.student_id == db_user_profile.id).first()
        if not existing_academic:
            academic = AcademicInfo(
                student_id=db_user_profile.id,
                previous_school=user_profile.academic_info.previous_school,
                admission_year=user_profile.academic_info.admission_year,
                gpa=user_profile.academic_info.gpa,
                section=user_profile.academic_info.section,
            )
            db.add(academic)

        db.commit()
        db.refresh(db_user_profile)
        return db_user_profile
    except Exception:
        db.rollback()
        raise


def get_user_profiles(db: Session):
    statement = select(UserProfile)
    return db.execute(statement).scalars().all()


def get_user_profile_by_id(db: Session, user_profile_id: int):
    statement = select(UserProfile).where(UserProfile.id == user_profile_id)
    return db.execute(statement).scalar_one_or_none()


def get_user_profile_by_email(db: Session, email: str):
    statement = select(UserProfile).where(UserProfile.email == email)
    return db.execute(statement).scalar_one_or_none()


def update_user_profile(db: Session, user_profile: UserProfile):
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    return user_profile


def delete_user_profile(db: Session, user_profile: UserProfile):
    db.delete(user_profile)
    db.commit()


def create_client(db: Session, user_profile):
    return create_user_profile(db, user_profile)


def get_clients(db: Session):
    return get_user_profiles(db)


def get_client_by_email(db: Session, email: str):
    return get_user_profile_by_email(db, email)