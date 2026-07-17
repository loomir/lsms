from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.academic_info import AcademicInfo
from app.schemas.client import ClientCreate


def create_student(db: Session, student: ClientCreate) -> Client:
    db_student = Client(
        name=student.name,
        email=student.email,
        dob=student.dob,
        gender=student.gender,
        grade=student.grade,
        phone=student.phone,
        address=student.address,
        status=student.status,
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    academic = AcademicInfo(
        student_id=db_student.id,
        previous_school=student.academic_info.previous_school,
        admission_year=student.academic_info.admission_year,
        gpa=student.academic_info.gpa,
        section=student.academic_info.section,
    )

    db.add(academic)
    db.commit()
    db.refresh(academic)

    db.refresh(db_student)
    return db_student


def get_students(db: Session):
    statement = select(Client)
    return db.execute(statement).scalars().all()


def get_student_by_id(db: Session, student_id: int):
    statement = select(Client).where(Client.id == student_id)
    return db.execute(statement).scalar_one_or_none()


def get_student_by_email(db: Session, email: str):
    statement = select(Client).where(Client.email == email)
    return db.execute(statement).scalar_one_or_none()


def update_student(db: Session, student: Client):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Client):
    db.delete(student)
    db.commit()