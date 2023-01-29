# !/bin/sh

curl -o conf.json 172.17.0.2:8080/$INSTANCE_ID

LOCAL_IP=`cat conf.json | jq '.local_ip'`
LOCAL_PORT=`cat conf.json | jq -r '.local_port'`
LOCAL_NAME=`cat conf.json | jq '.local_name'`
REMOTE_IP=`cat conf.json | jq '.remote_ip'`
REMOTE_PORT=`cat conf.json | jq -r '.remote_port'`
REMOTE_NAME=`cat conf.json | jq '.remote_name'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`

curl -LO $FILE_URL

echo "\n\033[0;32m*** GATEWAY SUCCEFULLY STARTED *** \033[1;37m"
echo '----------------------------------'
echo 'LOCAL_NAME\t'${LOCAL_NAME}
echo 'LOCAL_IP\t'${LOCAL_IP}
echo 'LOCAL_PORT\t'${LOCAL_PORT}'\n'
echo 'REMOTE_NAME\t'${REMOTE_NAME}
echo 'REMOTE_IP\t'${REMOTE_IP}
echo 'REMOTE_PORT\t'${REMOTE_PORT}
echo '----------------------------------\n'

node gateway.js --local_ip $LOCAL_IP --local_port $LOCAL_PORT --local_name $LOCAL_NAME --remote_ip $REMOTE_IP --remote_port $REMOTE_PORT --remote_name $REMOTE_NAME &