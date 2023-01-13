#!/bin/sh

LOCAL_IP=`cat conf.json | jq '.local_ip'`
LOCAL_PORT=`cat conf.json | jq -r '.local_port'`
LOCAL_NAME=`cat conf.json | jq '.local_name'`
REMOTE_IP=`cat conf.json | jq '.remote_ip'`
REMOTE_PORT=`cat conf.json | jq -r '.remote_port'`
REMOTE_NAME=`cat conf.json | jq '.remote_name'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`
SEND_PERIOD=`cat conf.json | jq -r '.send_period'`

curl -LO $FILE_URL
node device.js --local_ip $LOCAL_IP --local_port $LOCAL_PORT --local_name $LOCAL_NAME --remote_ip $REMOTE_IP --remote_port $REMOTE_PORT --remote_name $REMOTE_NAME --send_period $SEND_PERIOD