from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.core.security import decode_token
from app.repositories.user_repository import get_user_by_id
from app.models.user import User
from app.core.roles import Role


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = get_user_by_id(db, int(user_id)) if str(user_id).isdigit() else None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user


def require_role(*roles: str | Role):
    allowed_roles = {role.value if isinstance(role, Role) else role for role in roles}

    def permission(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user

    return permission


def require_admin():
    return require_role(Role.admin, Role.superadmin)


def require_staff():
    return require_role(Role.staff, Role.admin, Role.superadmin)


def require_teacher():
    return require_role(Role.teacher, Role.staff, Role.admin, Role.superadmin)


def require_student():
    return require_role(Role.student)


# Convenience dependency for admin-level access
get_current_admin = require_admin()

# Backwards-compatible alias for existing code
role_permission = require_role
