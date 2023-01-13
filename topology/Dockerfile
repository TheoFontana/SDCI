# syntax=docker/dockerfile:1

FROM ubuntu:trusty

ARG INSTANCE_TYPE
ENV INSTANCE_ID =''

RUN mkdir /componnent
WORKDIR /componnent

ADD start_$INSTANCE_TYPE.sh /componnent

RUN apt-get update \
    && apt-get install curl -y \
    && apt-get install jq -y \
    && apt-get install nodejs -y \
    && apt-get install npm -y \
    && npm install express \
    && npm install systeminformation \
    && npm install yargs \
    && npm install request

EXPOSE 9001
ENTRYPOINT sh /componnent/start_$INSTANCE_TYPE.sh && /bin/sh