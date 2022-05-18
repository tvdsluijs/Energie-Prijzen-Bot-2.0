#**************************************
# Build By:
# https://itheo.tech 2021
# MIT License
# Dockerfile to run the python script
#**************************************

FROM python:3.10.4-slim as base

LABEL org.opencontainers.image.authors="info@itheo.tech"
ENV TZ=Europe/Amsterdam

RUN apt-get update && apt-get install -y tzdata

WORKDIR /src

COPY requirements.txt .
COPY ./src .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /src/requirements.txt

FROM base as dev
ENV PY_ENV=dev
CMD [ "python", "main.py" ]

FROM base as acc
ENV PY_ENV=acc
CMD [ "python", "main.py" ]

FROM base as PROD
ENV PY_ENV=prod
CMD [ "python", "main.py" ]