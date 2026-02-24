from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
	app_name: str = Field(default="User Management API")
	debug: bool = Field(default=True)

	database_url: str | None = None

	jwt_secret_key: str = Field(default="changeme", alias="JWT_SECRET_KEY")
	jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
	jwt_access_token_expire_minutes: int = Field(default=60, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

	class Config:
		env_file = ".env"
		extra = "ignore"

settings = Settings()
