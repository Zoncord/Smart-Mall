FROM python:3.10.4-alpine
MAINTAINER Firsov Kirill <kirill.firsov@zoncord.tech>
RUN mkdir /home/smart_mall/
WORKDIR /home/smart_mall/

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN apk add jpeg-dev zlib-dev

RUN pip install 'poetry'

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .
