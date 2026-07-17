from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

if False:
    from app.models.user_profile import UserProfile


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, unique=True)
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)

    user_profile = relationship(
        "app.models.user_profile.UserProfile",
        primaryjoin="Guardian.student_id == UserProfile.id",
        foreign_keys="[Guardian.student_id]",
        back_populates="guardian",
    )
