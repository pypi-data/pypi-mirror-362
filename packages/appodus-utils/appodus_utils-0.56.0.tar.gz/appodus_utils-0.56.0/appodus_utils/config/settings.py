import enum
import os
from typing import Optional, Any, Dict

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings, validator, PostgresDsn, AnyUrl


def get_absolute_path(path: str):
    directory = os.getcwd()
    test = 'test'
    main = 'main'
    if test in directory:
        directory = directory.split(sep=test)[0]
    if main in directory:
        directory = directory.split(sep=main)[0]
    directory = os.path.join(directory, path)

    return directory


class SupportedDB(str, enum.Enum):
    MYSQL = 'MYSQL'
    MSSQL = 'MSSQL'
    POSTGRES = 'POSTGRES'
    ORACLE = 'ORACLE'

class Environment(str, enum.Enum):
    PRODUCTION = "prod"
    STAGING = "staging"
    TEST = "test"
    DEVELOPMENT = "dev"
    LOCAL = "local"


class AppodusBaseSettings(BaseSettings):
    APP_NAME: str = "appodus"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    ALLOW_AUTH_BYPASS: bool = False  # Optional

    APP_DOMAIN: str = "http://localhost:8000"
    SHOW_API: bool = True
    APPODUS_CLIENT_ID: str
    APPODUS_CLIENT_SECRET: str
    APPODUS_CLIENT_SECRET_ENCRYPTION_KEY: str
    APPODUS_CLIENT_REQUEST_EXPIRES_SECONDS: Optional[int] = 60 * 5 # 5mins


    # Enable / Disable Services
    DISABLE_RATE_LIMITING: bool = False

    # LOGGING
    LOG_LEVEL: Optional[str] = 'DEBUG'
    LOGGER_FILE: Optional[str] = 'logs.txt'
    LOGGER_FILE_PATH: Optional[str] = '/tmp/logs'

    # TOKEN
    CACHE_DATA_EXPIRES_SECONDS: Optional[int] = 60 * 60 * 24 * 8

    # WEBHOOK
    WEBHOOK_PATH: Optional[str] = "/webhooks"

    # REDIS
    REDIS_ENABLED: Optional[bool] = False
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[str]
    REDIS_USERNAME: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: Optional[str] = '0'
    REDIS_THREAD_SLEEP_TIME: Optional[float] = 0.01

    # DB
    ACTIVE_DB: Optional[SupportedDB] = SupportedDB.POSTGRES
    DB_SCHEME: Optional[str]
    DB_SERVER: Optional[str] = "sqlite:///"
    DB_USER: Optional[str]
    DB_PASSWORD: Optional[str]
    DB_PORT: Optional[str]
    DB_NAME: Optional[str]
    DB_ADDITIONAL_CONFIG: Optional[str]
    SQLALCHEMY_DATABASE_URI: Any
    DB_ENABLE_LOGS: Optional[bool] = True
    DB_ENABLE_LOG_POOL: Optional[bool] = True
    DB_MAIN_THREAD_CONTEXT_ID: int = 12345

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        db_url = v
        if isinstance(v, str):
            return v

        if SupportedDB.POSTGRES == values.get("ACTIVE_DB"):
            db_url = PostgresDsn.build(
                scheme=values.get("DB_SCHEME"),
                user=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_SERVER"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME') or ''}?{values.get('DB_ADDITIONAL_CONFIG')}",
            )
        elif SupportedDB.MYSQL == values.get("ACTIVE_DB"):
            db_url = AnyUrl.build(
                scheme=values.get("DB_SCHEME"),
                user=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_SERVER"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME') or ''}?{values.get('DB_ADDITIONAL_CONFIG')}",
            )
        else:
            db_path = get_absolute_path(os.path.join("main", "app", "db"))
            db = os.path.join(db_path, values.get('DB_NAME'))
            db_url = f"{values.get('DB_SERVER')}{db}?{values.get('DB_ADDITIONAL_CONFIG')}"

            print('db_url: ', db_url)

        return db_url

    class Config:
        env_file = get_absolute_path(f'.env.{os.getenv("appodus_active_env", "local")}')

        load_dotenv(dotenv_path=env_file)
        print(f'env_file: {env_file}')
        env_file_encoding = "utf-8"
        case_sensitive = False

    def set_env_vars(self):
        """Set all settings as environment variables."""
        for key, value in self.dict().items():
            os.environ[key.upper()] = str(value)
