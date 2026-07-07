from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class ResponseWrapper(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)
