from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_session, engine, Base

app = FastAPI(
    title="Measurment Service",
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


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db-test")
async def check_db_connection(session: Session = Depends(get_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "database": "connected", "test_query": f"{value}"}
    except Exception as e:
        return {"status": "error", "database": "diconnected", "error": str(e)}
