FROM python:3.7.6-alpine
RUN apk update && apk add build-base postgresql-dev bash
COPY ./webapp/requirements.txt /requirements/requirements.txt
RUN pip install -r /requirements/requirements.txt
RUN mkdir /sent_emails/
WORKDIR /app/
