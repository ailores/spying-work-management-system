from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = ""

    CAT_API_URL: str = ""
    API_V1_STR: str = "/api/v1"

    DB_URL: str = "sqlite:///app/core/db/spa.db"

    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore",
    )


settings: Settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
