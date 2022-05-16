#**************************************
# Build By:
# https://itheo.tech 2021
# MIT License
# Dockerfile to run the python script
#**************************************

FROM python:3.10.4-slim

LABEL org.opencontainers.image.authors="info@itheo.tech"
ENV TZ=Europe/Amsterdam
ENV PY_ENV=prod

RUN apt-get update && apt-get install -y tzdata

WORKDIR /src
# VOLUME ["/src/data"]

COPY requirements.txt .
COPY ./src .

# RUN apk update && apk add python3-dev \
#                           gcc \
#                           libc-dev \
#                           libffi-dev

# RUN apk add --update alpine-sdk
RUN pip install --upgrade pip

# COPY requirements.txt ./
RUN pip install --no-cache-dir -r /src/requirements.txt

CMD [ "python", "main.py" ]