from app.models.academic_info import AcademicInfo
from sqlalchemy.orm import Session

from app.repositories.student_repository import (
    create_student,
    get_students,
    get_student_by_email,
)
from app.schemas.student import StudentCreate


class StudentService:

    def create_student(self, db: Session, student: StudentCreate):
        existing = get_student_by_email(db, student.email)
        if existing:
            raise ValueError("Student email already exists")

        return create_student(db, student)

    def get_students(self, db: Session):
        return get_students(db)


student_service = StudentService()