from app.models.academic_info import AcademicInfo
from sqlalchemy.orm import Session

from app.repositories.client_repository import (
    create_client,
    get_clients,
    get_client_by_email,
)
from app.schemas.student import ClientCreate


class StudentService:

    def create_student(self, db: Session, student: ClientCreate):
        existing = get_client_by_email(db, student.email)
        if existing:
            raise ValueError("Student email already exists")

        return create_client(db, student)

    def get_students(self, db: Session):
        return get_clients(db)


student_service = StudentService()