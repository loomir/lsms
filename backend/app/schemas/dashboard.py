from pydantic import BaseModel
from typing import Optional


class MonthlyStatistic(BaseModel):
    period: str
    count: int

    model_config = {
        "from_attributes": True
    }


class DashboardResponse(BaseModel):
    total_students: int
    pending_admissions: int
    approved_admissions: int
    recent_registrations: list[dict]
    monthly_admissions: list[MonthlyStatistic]
    monthly_registrations: list[MonthlyStatistic]

    model_config = {
        "from_attributes": True
    }
