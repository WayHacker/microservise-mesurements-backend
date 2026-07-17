from pydantic import BaseModel
#TODO: Add phone validation

class PhoneRequest(BaseModel):
    phone: str


class CodeVerifyRequest(BaseModel):
    phone: str
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str