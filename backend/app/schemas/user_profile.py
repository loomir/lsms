from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional


class GuardianInfo(BaseModel):
    name: str
    relationship: str
    phone: str
    address: str

    model_config = {
        "from_attributes": True
    }


class AcademicInfo(BaseModel):
    previous_school: str
    admission_year: int
    gpa: float
    section: str

    model_config = {
        "from_attributes": True
    }


class UserProfileCreate(BaseModel):
    name: str
    email: EmailStr
    dob: date
    gender: str
    grade: str
    phone: str
    address: str
    status: Optional[str] = "active"
    academic_info: AcademicInfo

    model_config = {
        "from_attributes": True
    }


class UserProfileUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    dob: Optional[date]
    gender: Optional[str]
    grade: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    status: Optional[str]
    guardian: Optional[GuardianInfo]
    academic_info: Optional[AcademicInfo]

    model_config = {
        "from_attributes": True
    }


class GuardianResponse(GuardianInfo):
    pass


class AcademicInfoResponse(AcademicInfo):
    pass


class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    dob: date
    gender: str
    grade: str
    phone: str
    address: str
    status: str
    academic_info: AcademicInfoResponse

    model_config = {
        "from_attributes": True
    }


class UserProfileListResponse(BaseModel):
    user_profiles: list[UserProfileResponse]
    total: int
    page: int
    page_size: int

    model_config = {
        "from_attributes": True
    }


ClientCreate = UserProfileCreate
ClientUpdate = UserProfileUpdate
ClientResponse = UserProfileResponse
ClientListResponse = UserProfileListResponse
