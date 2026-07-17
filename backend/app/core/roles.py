from enum import Enum


class Role(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    staff = "staff"
    teacher = "teacher"
    student = "student"
    client = "client"


ALL_ROLES = [role.value for role in Role]
