"""Load config."""
from os import environ

import toml

config = toml.load('config.toml')

URL_SELENOID = environ.get('URL_SELENOID')

ANTICAPTCHA_TOKEN = environ.get('ANTICAPTCHA_TOKEN')

PROXY_GET_JSON_URL = environ.get('PROXY_GET_JSON_URL')

USER_MAIL = environ.get('USER_MAIL')
PASS_MAIL = environ.get('PASS_MAIL')

SQLALCHEMY_DATABASE_URI = (
    'postgresql+psycopg2://postgres:{password}@{db}/postgres'.format(
        db=environ.get('DB'),
        password=environ.get('DB_PASSWORD')
    )
)
