from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent 
ENV_PATH = BASE_DIR / ".env"

class DatabaseConfig(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )

    @property
    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.NAME}"
        )

class RedisConfig(BaseSettings):
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )


class AuthJWT(BaseSettings):
    PRIVATE_KEY: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 


class AppConfig(BaseSettings):
    HOST: str
    PORT: int
    DEBUG: bool

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )

    @property
    def get_log_level(self):
        if self.DEBUG:
            return "debug"
        return "error"
    
class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, 
        env_file_encoding="utf-8",
    )

    database: DatabaseConfig = DatabaseConfig()
    app: AppConfig = AppConfig()
    redis: RedisConfig = RedisConfig()
    auth_jwt: AuthJWT = AuthJWT()

config = Config()