# syntax=docker/dockerfile:1

FROM ubuntu:trusty

ARG SCRIPT
ARG NODE_VERSION=14
ENV INSTANCE_ID=''

RUN mkdir /componnent
WORKDIR /componnent

ADD $SCRIPT .

RUN apt-get update -y\
    && apt-get upgrade -y\
    && apt-get install curl -y\
    && apt-get install jq -y
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
RUN curl -sL https://deb.nodesource.com/setup_$NODE_VERSION.x | bash - \
    && apt-get install nodejs -yq\    
    && npm init -y\ 
    && npm install express \
    && npm install systeminformation \
    && npm install yargs\
    && npm install request

ENTRYPOINT sh /componnent/$SCRIPT && /bin/sh
