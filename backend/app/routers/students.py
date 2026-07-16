from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.student import StudentCreate
from app.services.student_service import student_service

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/test")
def students_test():
    return {"message": "Students router working"}


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return student_service.create_student(db, student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_students(
    db: Session = Depends(get_db)
):
    return student_service.get_students(db)