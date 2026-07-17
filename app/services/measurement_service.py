from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementUpdate, MeasurementCreate


async def get_measurements(
    user_id: int, db: AsyncSession, limit: int = 100, offset: int = 0
) -> list[Measurement]:
    stmt = (
        select(Measurement)
        .where(Measurement.user_id == user_id, Measurement.is_deleted == False)
        .order_by(Measurement.created_at)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(stmt)
    measurements = result.scalars().all()
    return measurements


async def get_measurement(
    measurement_id: int, user_id: int, db: AsyncSession
) -> Measurement | None:
    stmt = select(Measurement).where(
        Measurement.user_id == user_id,
        Measurement.id == measurement_id,
        Measurement.is_deleted == False,
    )
    result = await db.execute(stmt)
    measurement = result.scalar_one_or_none()
    return measurement


async def create_measurement(
    user_id: int, data: MeasurementCreate, db: AsyncSession
) -> Measurement:
    measurement = Measurement(user_id=user_id, **data.model_dump())
    db.add(measurement)
    await db.commit()
    return measurement


async def update_measurement(
    measurement_id: int, user_id: int, data: MeasurementUpdate, db: AsyncSession
) -> Measurement | None:
    stmt = select(Measurement).where(
        Measurement.user_id == user_id,
        Measurement.id == measurement_id,
        Measurement.is_deleted == False,
    )
    result = await db.execute(stmt)
    measurement = result.scalar_one_or_none()

    if not measurement:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(measurement, key, value)
    measurement.updated_at = datetime.now(timezone.utc)
    await db.commit()
    return measurement


async def delete_measurement(
    measurement_id: int, user_id: int, db: AsyncSession
) -> bool:
    stmt = select(Measurement).where(
        Measurement.user_id == user_id,
        Measurement.id == measurement_id,
        Measurement.is_deleted == False,
    )
    result = await db.execute(stmt)
    measurement = result.scalar_one_or_none()

    if not measurement:
        return False

    measurement.is_deleted = True
    measurement.updated_at = datetime.now(timezone.utc)
    await db.commit()
    return True
