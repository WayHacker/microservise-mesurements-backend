import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.core.security import create_access_token, create_refresh_token
from app.core.config import settings

temp_codes = {}


def generate_code(phone: str) -> str:
    code = "".join(secrets.choice("0123456789") for _ in range(4))
    temp_codes[phone] = code
    print(temp_codes)
    return code


def verify_code(phone: str, code: str) -> bool:
    if temp_codes.get(phone) == code:
        del temp_codes[phone]
        return True
    return False


async def verify_and_auth(phone: str, code: str, db: AsyncSession):
    code_valid = verify_code(phone, code)
    if not code_valid:
        return None

    stmt = select(User).where(User.phone == phone)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        user = User(phone=phone)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    expire_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=expire_at,
    )
    db.add(refresh_token_obj)
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}
