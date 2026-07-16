from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.academic_info import AcademicInfo
from app.schemas.student import StudentCreate


def create_student(db: Session, student: StudentCreate) -> Student:
    db_student = Student(
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
    statement = select(Student)
    return db.execute(statement).scalars().all()


def get_student_by_id(db: Session, student_id: int):
    statement = select(Student).where(Student.id == student_id)
    return db.execute(statement).scalar_one_or_none()


def get_student_by_email(db: Session, email: str):
    statement = select(Student).where(Student.email == email)
    return db.execute(statement).scalar_one_or_none()


def update_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student):
    db.delete(student)
    db.commit()