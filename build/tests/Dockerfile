FROM python:3.7.6-alpine
RUN apk update && apk add build-base postgresql-dev bash
COPY ./webapp/ /app/
COPY ./build/wait-for-it.sh /wait-for-it.sh
COPY ./build/docker-test-entrypoint.sh /docker-test-entrypoint.sh
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT  /docker-test-entrypoint.sh
