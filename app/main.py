from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_session, engine, Base
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.profile import router as profile_router
from app.api.v1.endpoints.measurements import router as measurement_router
from app.api.v1.endpoints.shared import router as share_router
from app.api.deps import get_current_user
from app.schemas.common import ResponseWrapper
from app.admin import setup_admin

app = FastAPI(
    title="Measurement Service",
    description="Микросервис для хранения мерок пользователей",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dont forget to change it on prod!!!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth_router)
app.include_router(router=profile_router)
app.include_router(router=measurement_router)
app.include_router(router=share_router)

admin = setup_admin(app)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db-test")
async def check_db_connection(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "database": "connected", "test_query": f"{value}"}
    except Exception as e:
        return {"status": "error", "database": "diconnected", "error": str(e)}


@app.get("/api/v1/me")
async def get_me(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}


@app.exception_handler(HTTPException)
async def http_expception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseWrapper(
            success=False,
            data=None,
            error={"code": exc.status_code, "message": exc.detail},
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
        )
    return JSONResponse(
        status_code=422,
        content=ResponseWrapper(
            success=False,
            data=None,
            error={"code": 422, "message": "Validation error", "details": errors},
        ).model_dump(),
    )
