from os import environ

SQLALCHEMY_DATABASE_URI = (
    'postgresql+psycopg2://postgres:mysecretpassword@{db}/postgres'.format(
        db=environ.get('DB'),
    )
)

SECRET_KEY = environ.get('SECRET_KEY')
