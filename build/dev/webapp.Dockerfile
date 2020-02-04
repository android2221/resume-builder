FROM python:3.7.6-alpine
RUN apk update && apk add build-base postgresql-dev bash
COPY ./webapp /app/
WORKDIR /app/
RUN pip install -r requirements.txt
