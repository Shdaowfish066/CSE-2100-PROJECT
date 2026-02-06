"""JWT token generation/validation and Argon2 password hashing."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.hash import argon2

from app.config import settings


def hash_password(password: str) -> str:
	return argon2.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return argon2.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes))
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
	return encoded_jwt


def decode_access_token(token: str) -> dict | None:
	try:
		payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		return payload
	except JWTError:
		return None
