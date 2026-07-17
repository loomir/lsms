from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class AcademicInfo(Base):
    __tablename__ = "academic_infos"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, unique=True)
    previous_school = Column(String, nullable=False)
    admission_year = Column(Integer, nullable=False)
    gpa = Column(Float, nullable=False)
    section = Column(String, nullable=False)

    client = relationship("Client", back_populates="academic_info")
