from sqlalchemy.orm import Session

from app.repositories.client_repository import (
    create_client,
    get_clients,
    get_client_by_email,
)
from app.schemas.student import ClientCreate


class ClientService:

    def create_client(self, db: Session, student: ClientCreate):
        existing = get_client_by_email(db, student.email)
        if existing:
            raise ValueError("Student email already exists")

        return create_client(db, student)

    def get_clients(self, db: Session):
        return get_clients(db)


student_service = ClientService()