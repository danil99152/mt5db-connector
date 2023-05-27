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
    host_history = f'{address}/api/history/list'

    address = 'localhost'
    SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:root@{address}:5432/mt5db'

    leader_image = 'eb2e977b806b221556ae5c6217c36645a9f046fe75dc4af3a4d702dc45140c59'
    investor_image = 'd730d83728ad252dbc8ca3c89a86ea65225753ae20d80e2faafc1e6b117fa34b'


settings = Settings()
