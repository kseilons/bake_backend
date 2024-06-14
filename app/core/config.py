import os
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import Field, PostgresDsn, EmailStr, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
import secrets
from enum import Enum


class DatabaseSettings(BaseSettings):
    DB_USER: str = Field("postgres")
    DB_PASS: str = Field("admin")
    DB_HOST: str = Field("localhost")
    DB_PORT: int = Field(5432)
    DB_NAME: str = Field("bd_name")
    
    DATABASE_URL: PostgresDsn | str = Field("")

    
    @field_validator("DATABASE_URL", mode="after")
    def assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str) and v == "":
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data["DB_USER"],
                password=info.data["DB_PASS"],
                host=info.data["DB_HOST"],
                port=info.data["DB_PORT"],
                path=info.data["DB_NAME"],
            )
        return v

    
class EmailSettings(BaseSettings):
    SMTP_SERVER: str = Field("smtp.gmail.com")
    SMTP_PORT: int = Field(465 )
    SMTP_USERNAME: str = Field("your_email@gmail.com")
    SMTP_PASSWORD: str = Field("your_password")
    MANAGER_EMAIL: str = Field("manager@gmail.com")
    
class AuthSettings(BaseSettings):
    SECRET: str = Field("sadfvxzcnbdflfkgljiojIJHbL")
    VERIFY_PATH: str = Field("/confirm/")
    FORGOT_PASSWORD_PATH: str = Field("/reset-pasword/")
    
class TemplateName(BaseSettings):
    EMAIL_CONFIRM: str = Field("email_confirm.html")
    FORGOT_PASSWORD: str = Field("forgot_password.html")
    ORDER_CALL: str = Field("order_call.html")
    ORDER_FOR_USER: str = Field("order_for_user.html")
    ORDER_FOR_MANAGER: str = Field("order_for_manager.html")
    
class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    email: EmailSettings = EmailSettings()
    auth: AuthSettings = AuthSettings()
    template: TemplateName = TemplateName()
    FRONTEND_URL: str = Field("http://localhost:80/")
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
