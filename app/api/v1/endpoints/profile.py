from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import (
    PhoneRequest,
    CodeVerifyRequest,
    TokenResponse,
    RefreshRequest,
)
from app.schemas.common import ResponseWrapper
from app.core.database import get_session
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.api.deps import get_current_user
from app.services.profile_service import get_profile, upsert_profile

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


@router.get("")
async def get_current_profile(
    user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_session)
):
    profile = await get_profile(user_id, db)
    if profile is None:
        return ResponseWrapper(
            success=True,
            data=ProfileResponse(
                id=0,
                user_id=user_id,
                gender=None,
                age=None,
                updated_at=datetime.now(timezone.utc),
            ),
        )
    return ResponseWrapper(
        success=True, data=ProfileResponse.model_validate(profile), error=None
    )


@router.put("")
async def update_profile(
    data: ProfileUpdate,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    profile = await upsert_profile(user_id, data, db)
    return ResponseWrapper(
        success=True, data=ProfileResponse.model_validate(profile), error=None
    )
