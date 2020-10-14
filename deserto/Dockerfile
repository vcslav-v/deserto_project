FROM python:3.8-slim

RUN pip install poetry

RUN mkdir -p /usr/src/app/deserto

WORKDIR /usr/src/app/

COPY poetry.lock pyproject.toml config.toml anticaptcha.crx /usr/src/app/

COPY deserto/. deserto/.

RUN poetry install --no-dev 

CMD poetry run deserto