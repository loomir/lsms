from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

if False:
    from app.models.user_profile import UserProfile


class AcademicInfo(Base):
    __tablename__ = "academic_infos"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True)
    previous_school = Column(String, nullable=False)
    admission_year = Column(Integer, nullable=False)
    gpa = Column(Float, nullable=False)
    section = Column(String, nullable=False)

    user_profile = relationship(
        "app.models.user_profile.UserProfile",
        primaryjoin="AcademicInfo.student_id == UserProfile.id",
        foreign_keys="[AcademicInfo.student_id]",
        back_populates="academic_info",
    )
