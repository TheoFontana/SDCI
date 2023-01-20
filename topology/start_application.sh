# !/bin/sh

curl -o conf.json metadata_server/$INSTANCE_ID

REMOTE_IP=`cat conf.json | jq '.remote_ip'`
REMOTE_PORT=`cat conf.json | jq -r '.remote_port'`
REMOTE_NAME=`cat conf.json | jq '.remote_name'`
SEND_PERIOD=`cat conf.json | jq -r '.send_period'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`

curl -LO $FILE_URL
node device.js --local_ip $LOCAL_IP --local_port $LOCAL_PORT --local_name $LOCAL_NAME --remote_ip $REMOTE_IP --remote_port $REMOTE_PORT --remote_name $REMOTE_NAME --send_period $SEND_PERIOD

echo "\n\033[0;32m*** DEVICE SUCCEFULLY STARTED *** \033[1;37m"
echo '---------------------------------'
echo 'REMOTE_NAME\t'${REMOTE_NAME} 
echo 'REMOTE_IP\t'${REMOTE_IP} 
echo 'REMOTE_PORT\t'${REMOTE_PORT}'\n'
echo 'SEND_PERIOD\t'${SEND_PERIOD}
echo '---------------------------------\n'
