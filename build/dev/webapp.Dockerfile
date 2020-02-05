FROM python:3.7.6-alpine
RUN apk update && apk add build-base postgresql-dev bash
COPY ./build/docker-entrypoint.dev.sh /docker-entrypoint.dev.sh
COPY ./build/wait-for-it.sh /wait-for-it.sh
COPY ./webapp /app/
WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT /docker-entrypoint.dev.sh
