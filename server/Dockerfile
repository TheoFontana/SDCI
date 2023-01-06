# syntax=docker/dockerfile:1

FROM node:18-alpine

RUN mkdir /server
WORKDIR /server

ADD start.sh /server

RUN apk update \
    && apk add curl \
    && apk add jq \
    && npm install express \
    && npm install systeminformation \
    && npm install yargs

RUN curl -o conf.json metadata_server/server

ENTRYPOINT sh /server/start.sh && /bin/sh

EXPOSE 8080