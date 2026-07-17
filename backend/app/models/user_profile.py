from datetime import datetime, date
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.academic_info import AcademicInfo
from app.models.guardian import Guardian


class UserProfile(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    guardian = relationship(
        Guardian,
        uselist=False,
        primaryjoin="UserProfile.id == Guardian.student_id",
        foreign_keys="[Guardian.student_id]",
        back_populates="user_profile",
    )
    academic_info = relationship(
        AcademicInfo,
        uselist=False,
        primaryjoin="UserProfile.id == AcademicInfo.student_id",
        foreign_keys="[AcademicInfo.student_id]",
        back_populates="user_profile",
    )
