from pydantic import BaseModel, EmailStr, Field
from typing import Literal


# ✅ Allowed roles (STRICT)
UserRole = Literal[
    "student",
    "trainer",
    "institution",
    "programme_manager",
    "monitoring_officer"
]


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    role: UserRole   # ✅ restricted roles


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"