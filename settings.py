import pathlib

from pydantic import BaseSettings, conint, constr
from pydantic.validators import IPv4Address


class Settings(BaseSettings):
    APP_TITLE: constr(min_length=1, max_length=255) = 'MT5Connector'
    APP_VERSION: constr(min_length=1, max_length=15) = '1'
    APP_HOST: constr(min_length=1, max_length=15) = str(IPv4Address('0.0.0.0'))
    APP_PORT: conint(ge=0) = 8000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())

    host = 'https://my.atimex.io:8000/api/demo_mt5/last'
    host_investor = 'https://my.atimex.io:8000/api/investor/list'
    host_leader = 'https://my.atimex.io:8000/api/leader/list'
    host_history = 'https://my.atimex.io:8000/api/history/list'
    host_exchanges = 'https://my.atimex.io:8000/api/exchanges/list'
    host_strategy = 'https://my.atimex.io:8000/api/strategy-list'

    address = '91.228.224.105'
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@{address}:5432/mt5db'


settings = Settings()
