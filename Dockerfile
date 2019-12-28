FROM python:3.7.6-alpine
RUN apk add build-base
RUN apk add postgresql-dev
WORKDIR /app/
COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt