# syntax=docker/dockerfile:1

FROM node:18-alpine

ARG GW_ID

RUN mkdir /gateway
WORKDIR /gateway

ADD start.sh /gateway

RUN apk update \
    && apk add curl \
    && apk add jq \
    && npm install express \
    && npm install systeminformation \
    && npm install yargs \
    && npm install request

RUN echo $GW_ID
RUN curl -o conf.json metadata_server/$GW_ID

RUN cat conf.json

ENTRYPOINT sh /gateway/start.sh && /bin/sh

EXPOSE 8181