from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.measurement import (
    MeasurementResponse,
    MeasurementCreate,
    MeasurementUpdate,
)
from app.core.database import get_session
from app.api.deps import get_current_user
from app.services.measurement_service import (
    get_measurements,
    create_measurement,
    get_measurement,
    update_measurement,
    delete_measurement,
    share_measurement,
)
from app.schemas.common import ResponseWrapper

router = APIRouter(prefix="/api/v1/measurements", tags=["measurements"])


@router.get("/api/v1/measurements")
async def get_user_measurements(
    limit: int = 100,
    offset: int = 0,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):

    measurements = await get_measurements(user_id, db, limit=limit, offset=offset)
    return ResponseWrapper(
        success=True,
        data=[MeasurementResponse.model_validate(m) for m in measurements],
        error=None,
    )


@router.post("/api/v1/measurements", status_code=201)
async def create_user_measurement(
    data: MeasurementCreate,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    measurement = await create_measurement(user_id, data, db)
    return ResponseWrapper(
        success=True, data=MeasurementResponse.model_validate(measurement), error=None
    )


@router.get("/api/v1/measurements/{measurement_id}")
async def get_user_measurement(
    measurement_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    measurement = await get_measurement(measurement_id, user_id, db)
    if measurement is None:
        return HTTPException(status_code=404, detail="Measurement not found")
    return ResponseWrapper(
        success=True, data=MeasurementResponse.model_validate(measurement), error=None
    )


@router.put("/api/v1/measurement/{measurement_id}")
async def update_user_measurement(
    measurement_id: int,
    data: MeasurementUpdate,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    measurement = await update_measurement(measurement_id, user_id, data, db)
    if measurement is None:
        return HTTPException(status_code=404, detail="Measurement not found")
    return ResponseWrapper(
        success=True, data=MeasurementResponse.model_validate(measurement), error=None
    )


@router.delete("/api/v1/measurements/{measurement_id}", status_code=204)
async def delete_user_measurement(
    measurement_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await delete_measurement(measurement_id, user_id, db)
    if result is False:
        raise HTTPException(status_code=404, detail="Measurement not found")

    return ResponseWrapper(success=True, data=None, error=None)


@router.post("/api/v1/measurements/{measurement_id}/share")
async def share_user_measurement(
    measurement_id: int,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    result = await share_measurement(measurement_id, user_id, db)
    if result is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return ResponseWrapper(success=True, data={"share_url": f"/api/v1/shared/{result}"})
