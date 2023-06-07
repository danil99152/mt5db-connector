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

    leader_cms_image = '209bba5598a658d4d9ee75da04b6107badf652a88e4fed6f0ac711d5866891e7'
    investor_cms_image = 'a0f41873afe7744e3fe24b3ed87cebbff7f4fbf96b69cbbadf0ecc876172fc25'

    leader_signal_image = ''
    investor_signal_image = ''


settings = Settings()
