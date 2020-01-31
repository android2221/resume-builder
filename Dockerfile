FROM python:3.7.6-alpine
RUN apk add build-base postgresql-dev
COPY ./requirements.txt /requirements/requirements.txt
COPY ./webapp/ /app/
RUN pip install -r /requirements/requirements.txt
WORKDIR /app/
RUN python manage.py collectstatic --noinput
