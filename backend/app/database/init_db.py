from app.core.database import Base, engine

# সব Model import করতে হবে
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.student import Student
from app.models.guardian import Guardian
from app.models.academic_info import AcademicInfo
from app.models.admission import Admission


def init_db():
    Base.metadata.create_all(bind=engine)