#!/bin/sh

REMOTE_IP=`cat conf.json | jq '.remote_ip'`
REMOTE_PORT=`cat conf.json | jq -r '.remote_port'`
REMOTE_NAME=`cat conf.json | jq '.remote_name'`
SEND_PERIOD=`cat conf.json | jq -r '.send_period'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`


curl -LO $FILE_URL
node application.js --remote_ip $REMOTE_IP --remote_port $REMOTE_PORT --device_name $REMOTE_NAME --send_period $SEND_PERIOD