from datetime import datetime, date
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Client(Base):
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

    guardian = relationship("Guardian", uselist=False, back_populates="client")
    academic_info = relationship("AcademicInfo", uselist=False, back_populates="client")
