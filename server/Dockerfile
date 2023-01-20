# syntax=docker/dockerfile:1

FROM ubuntu:trusty

ARG SCRIPT_NAME
ENV INSTANCE_ID=''

RUN mkdir /componnent
WORKDIR /componnent

ADD $SCRIPT_NAME.sh /componnent

RUN apt-get update -y \
    && apt-get insatalll curl -y\
    && apt-get insatalll jq -y\
    && npm install express \
    && npm install systeminformation \
    && npm install yargs\
    && npm install request

ENTRYPOINT sh /componnent/$SCRIPT_NAME.sh && /bin/sh