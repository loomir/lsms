from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def create_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
    rt = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        revoked=False,
        created_at=datetime.utcnow()
    )
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    statement = select(RefreshToken).where(RefreshToken.token == token)
    return db.execute(statement).scalar_one_or_none()


def revoke_refresh_token(db: Session, token: str) -> None:
    rt = get_refresh_token(db, token)
    if not rt:
        return
    rt.revoked = True
    db.add(rt)
    db.commit()


def revoke_all_for_user(db: Session, user_id: int) -> int:
    statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
    rows = db.execute(statement).scalars().all()
    count = 0
    for r in rows:
        if not r.revoked:
            r.revoked = True
            db.add(r)
            count += 1
    db.commit()
    return count
