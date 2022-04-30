FROM python:3.10.4-alpine
MAINTAINER Firsov Kirill <kirill.firsov@zoncord.tech>
WORKDIR /urs/src/smart_mall

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

RUN pip install 'poetry'

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

CMD gunicorn SmartMall.wsgi:application --bind 0.0.0.0:8000