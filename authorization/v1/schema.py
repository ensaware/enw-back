from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    token: str
    token_type: str = 'Bearer'
    refresh_token: str


class TokenData(BaseModel):
    email: EmailStr
    exp: int
    iat: int
    profile: str
    sub: str


class RefreshToken(BaseModel):
    refresh_token: str