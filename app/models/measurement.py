from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Measurement(Base):
    __tablename__ = "measurements"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    chest: Mapped[Optional[int]] = mapped_column(Integer)
    waist: Mapped[Optional[int]] = mapped_column(Integer)
    hips: Mapped[Optional[int]] = mapped_column(Integer)
    shoulder_width: Mapped[Optional[int]] = mapped_column(Integer)
    sleeve_lenght: Mapped[Optional[int]] = mapped_column(Integer)
    inseam: Mapped[Optional[int]] = mapped_column(Integer)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    share_token: Mapped[uuid.UUID] = mapped_column(
        String(36), unique=True, default=uuid.uuid4, nullable=False, index=True
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="measurements")