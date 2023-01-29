# syntax=docker/dockerfile:1
FROM ubuntu:trusty
ARG ADD_GWI=10.1.0.10
ARG PORT_GWI=8181
ARG NODE_VERSION=14
ARG INSTANCE_ID=gwi_vnf
ENV ENV_ADD_GWI=$ADD_GWI
ENV ENV_PORT_GWI=$PORT_GWI
ENV VIM_EMU_CMD ./start_vnf.sh
ENV VIM_EMU_CMD_STOP ./stop_vnf.sh
ENV INSTANCE_ID=$INSTANCE_ID

RUN mkdir /adaptation
WORKDIR /adaptation

ADD start_vnf.sh /adaptation
ADD stop_vnf.sh /adaptation

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

EXPOSE 8181
CMD /bin/bash