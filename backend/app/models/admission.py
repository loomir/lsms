from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float
from app.core.database import Base


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    application_number = Column(String, unique=True, index=True, nullable=False)
    applicant_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    applied_grade = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
    score = Column(Float, nullable=True)
    document_path = Column(String, nullable=True)
    receipt_number = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)
