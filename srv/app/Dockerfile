FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip3 install poetry

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-dev
COPY ./migrations .
COPY ./src .
COPY ./main.py .
