FROM python:3.11-alpine

WORKDIR /app


COPY ./requirements/base.txt base.txt
#COPY ./requirements/local.txt local.txt

RUN pip install -r base.txt

COPY . .