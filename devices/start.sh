#!/bin/sh

LOCAL_IP=`cat conf.json | jq '.local_ip'`
LOCAL_PORT=`cat conf.json | jq -r '.local_port'`
LOCAL_NAME=`cat conf.json | jq '.local_name'`
REMOTE_IP=`cat conf.json | jq '.remote_ip'`
REMOTE_PORT=`cat conf.json | jq -r '.remote_port'`
REMOTE_NAME=`cat conf.json | jq '.remote_name'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`
SEND_PERIOD=`cat conf.json | jq -r '.send_period'`

echo $FILE_URL

cat  conf.json

curl -LO $FILE_URL
ls
node device.js --local_ip "127.0.0.1" --local_port 9001 --local_name "dev1" --remote_ip "127.0.0.1" --remote_port 8282 --remote_name "gwf1" --send_period $SEND_PERIOD