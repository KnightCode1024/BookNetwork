from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Bot(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        env_file=(ENV_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    TOKEN: str


class Database(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=(ENV_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.NAME}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ENV_DIR / ".env"),
        env_file_encoding="utf-8",
    )

    bot: Bot = Bot()
    database: Database = Database()


settings = Settings()
