import pathlib

from pydantic import BaseSettings, conint, constr
from pydantic.validators import IPv4Address


class Settings(BaseSettings):
    APP_TITLE: constr(min_length=1, max_length=255) = 'MT5Connector'
    APP_VERSION: constr(min_length=1, max_length=15) = '1'
    APP_HOST: constr(min_length=1, max_length=15) = str(IPv4Address('0.0.0.0'))
    APP_PORT: conint(ge=0) = 8000
    APP_PATH: constr(min_length=1, max_length=255) = str(pathlib.Path(__file__).parent.resolve())

    address = 'https://my.atimex.io:8000'
    host = f'{address}/api/demo_mt5/last'
    host_investor = f'{address}/api/investor/list'
    host_leader = f'{address}/api/leader/list'
    host_history = f'{address}/api/history/list'
    host_exchanges = f'{address}/api/exchanges/list'
    host_strategy = f'{address}/api/strategy-list'

    address = 'localhost'
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@{address}:5432/mt5db'


settings = Settings()
