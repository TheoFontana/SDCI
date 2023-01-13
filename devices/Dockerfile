# syntax=docker/dockerfile:1

FROM node:18-alpine

ARG DV_ID

RUN mkdir /device
WORKDIR /device

ADD start.sh /device

RUN apk update \
    && apk add curl \
    && apk add jq \
    && npm install express \
    && npm install systeminformation \
    && npm install yargs \
    && npm install request

RUN echo $DV_ID
RUN curl -o conf.json metadata_server/$DV_ID

RUN cat conf.json

EXPOSE 9001
ENTRYPOINT sh /device/start.sh && /bin/sh