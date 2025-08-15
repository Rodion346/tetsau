from pydantic import BaseModel
from pydantic import PostgresDsn, Field

from pydantic_settings import BaseSettings, SettingsConfigDict
from yookassa import Configuration


class DatabaseConfig(BaseModel):
    url: PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    db: DatabaseConfig
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ADMIN_BOT: str

    SMTP_SERVER: str = Field("smtp.yandex.com", description="SMTP server address or IP")
    SMTP_PORT: int = Field(465, description="SMTP server port")
    SMTP_USERNAME: str = Field(
        "PlusVibeEnglish@yandex.com", description="SMTP username"
    )
    SMTP_PASSWORD: str = Field("wugbqcmjvvbgpnjs", description="SMTP password")
    EMAIL_FROM: str = Field(
        "PlusVibeEnglish@yandex.com", description="Email sender address"
    )
    PROJECT_NAME: str = "PLUS-VIBE"

    ASSEMBLYAI_API_KEY: str
    OPENROUTER_API_KEY: str

    YOOKASSA_ACCOUNT_ID: str = "1133504"
    YOOKASSA_SECRET_KEY: str = "test_nrVFtEBPbuxErp4WPjeJ7H2kgPj4YhhPrZaZ5aJ3kDo"

    def get_auth_data(self):
        return {"secret_key": self.SECRET_KEY, "algorithm": self.ALGORITHM}


settings = Settings()

Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
