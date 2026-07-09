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
from app.services.auth_service import generate_code, verify_and_auth, refresh_tokens

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/api/v1/auth/request-code")
async def requst_code(request: PhoneRequest):
    generate_code(request.phone)

    return ResponseWrapper(success=True, data=None, error=None)


@router.post("/api/v1/verify-code")
async def verify_code(
    request: CodeVerifyRequest, db: AsyncSession = Depends(get_session)
):
    tokens = await verify_and_auth(request.phone, request.code, db)

    if tokens is None:
        raise HTTPException(status_code=400, detail="Invalid code")

    return ResponseWrapper(
        success=True,
        data=TokenResponse(
            access_token=tokens["access_token"], refresh_token=tokens["refresh_token"]
        ),
    )


@router.post("/api/v1/refresh")
async def refresh(request: RefreshRequest, db: AsyncSession = Depends(get_session)):
    tokens = await refresh_tokens(request.refresh_token, db)
    if tokens is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    return ResponseWrapper(
        success=True,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
    )
