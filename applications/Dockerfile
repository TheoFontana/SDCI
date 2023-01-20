# syntax=docker/dockerfile:1

FROM node:18-alpine

ARG APP_ID

RUN mkdir /application
WORKDIR /application

ADD start.sh /application

RUN apk update \
    && apk add curl \
    && apk add jq \
    && npm install express \
    && npm install systeminformation \
    && npm install yargs \
    && npm install request

RUN echo $APP_ID
RUN curl -o conf.json metadata_server/$APP_ID

RUN cat conf.json

ENTRYPOINT sh /application/start.sh && /bin/sh