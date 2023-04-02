import pathlib

from pydantic import BaseSettings, conint, constr
from pydantic.validators import IPv4Address


class Settings(BaseSettings):
    DEBUG: bool = True

    APP_TITLE: constr(min_length=1, max_length=255) = 'MT5Connector'
    APP_VERSION: constr(min_length=1, max_length=15) = '1'
    APP_HOST: constr(min_length=1, max_length=15) = str(IPv4Address('127.0.0.1' if DEBUG else '0.0.0.0'))
    APP_PORT: conint(ge=0) = 8000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())

    host = 'https://my.atimex.io:8000/api/demo_mt5/last'
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"


settings = Settings()
