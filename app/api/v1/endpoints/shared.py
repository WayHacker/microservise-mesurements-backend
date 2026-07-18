from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.measurement import MeasurementPublicRespone
from app.core.database import get_session
from app.services.measurement_service import get_public_measurement
from app.schemas.common import ResponseWrapper

router = APIRouter(prefix="/api/v1/shared", tags=["shared"])


@router.get("/{share_token}")
async def get_user_public_measurement(
    share_token: str, db: AsyncSession = Depends(get_session)
):
    measurement = await get_public_measurement(share_token, db)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return ResponseWrapper(
        success=True,
        data=MeasurementPublicRespone.model_validate(measurement),
        error=None,
    )
