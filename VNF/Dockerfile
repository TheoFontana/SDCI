# syntax=docker/dockerfile:1
FROM ubuntu:trusty
ARG ADD_GWI=10.1.0.10
ARG PORT_GWI=8181
ARG NODE_VERSION=14
ENV ENV_ADD_GWI=$ADD_GWI
ENV ENV_PORT_GWI=$PORT_GWI

ENV VIM_EMU_CMD ./start_vnf.sh
ENV VIM_EMU_CMD_STOP ./stop_vnf.sh

RUN mkdir /monitor
WORKDIR /monitor

ADD monitor.js /monitor
ADD start_vnf.sh /monitor
ADD stop_vnf.sh /monitor

RUN chmod +x start_vnf.sh \
    && chmod +x stop_vnf.sh
    
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

EXPOSE 8888
CMD /bin/bash