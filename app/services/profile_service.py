from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
from app.schemas.profile import ProfileUpdate


async def get_profile(user_id: int, db: AsyncSession) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()

    if profile is None:
        return None
    return profile


async def upsert_profile(
    user_id: int, data: ProfileUpdate, db: AsyncSession
) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await db.execute(stmt)
    profile = result.scalar_one_or_none()
    update_data = data.model_dump(exclude_unset=True)

    if profile:
        if update_data:
            for key, value in update_data.items():
                setattr(profile, key, value)
            profile.updated_at = datetime.now(timezone.utc)

    else:
        profile = Profile(user_id=user_id, **update_data)
        db.add(profile)

    await db.commit()

    await db.refresh(profile)
    return profile
