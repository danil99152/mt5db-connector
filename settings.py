import pathlib

from pydantic import BaseSettings, conint, constr
from pydantic.validators import IPv4Address


class Settings(BaseSettings):
    DEBUG: bool = False

    APP_TITLE: constr(min_length=1, max_length=255) = 'MT5Connector'
    APP_VERSION: constr(min_length=1, max_length=15) = '1'
    APP_HOST: constr(min_length=1, max_length=15) = str(IPv4Address('127.0.0.1' if DEBUG else '0.0.0.0'))
    APP_PORT: conint(ge=0) = 8000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())

    host = 'https://my.atimex.io:8000/api/demo_mt5/last'
    host_investor = 'https://my.atimex.io:8000/api/investor/list'
    host_history = 'https://my.atimex.io:8000/api/history/list'

    address = '91.228.224.105' if DEBUG else 'localhost'
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@{address}:5432/mt5db'


settings = Settings()
