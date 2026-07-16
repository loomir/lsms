from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class AdmissionCreate(BaseModel):
    applicant_name: str
    email: EmailStr
    phone: str
    applied_grade: str
    score: Optional[float] = None
    remarks: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class AdmissionStatusUpdate(BaseModel):
    status: str
    score: Optional[float] = None
    remarks: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class AdmissionResponse(BaseModel):
    application_number: str
    applicant_name: str
    email: EmailStr
    phone: str
    applied_grade: str
    status: str
    score: Optional[float]
    document_path: Optional[str]
    receipt_number: Optional[str]
    remarks: Optional[str]
    submitted_at: datetime
    reviewed_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


class AdmissionListResponse(BaseModel):
    admissions: list[AdmissionResponse]
    total: int
    page: int
    page_size: int

    model_config = {
        "from_attributes": True
    }
