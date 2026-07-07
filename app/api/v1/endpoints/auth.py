from fastapi import APIRouter

from app.schemas.auth import PhoneRequest
from app.schemas.common import ResponseWrapper
from app.services.auth_service import generate_code

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/api/v1/auth/request-code")
async def requst_code(request: PhoneRequest):
    generate_code(request.phone)

    return ResponseWrapper(success=True, data=None, error=None)
