"""Pydantic schemas for users."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating user fields - all fields are optional."""
    username: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
