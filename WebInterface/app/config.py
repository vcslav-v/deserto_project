from os import environ

SQLALCHEMY_DATABASE_URI = (
    'postgresql+psycopg2://postgres:{password}@{db}/postgres'.format(
        db=environ.get('DB'),
        password=environ.get('DB_PASSWORD')
    )
)

SECRET_KEY = environ.get('SECRET_KEY') or 'secret'
