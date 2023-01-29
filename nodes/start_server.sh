# !/bin/sh

curl -o conf.json metadata_server/$INSTANCE_ID

LOCAL_NAME=`cat conf.json | jq '.local_name'`
LOCAL_PORT=`cat conf.json | jq -r '.local_port'`
LOCAL_IP=`cat conf.json | jq '.local_ip'`
FILE_URL=`cat conf.json | jq -r '.file_URL'`

curl -LO $FILE_URL
node server.js --local_ip $LOCAL_IP --local_port $LOCAL_PORT --local_name $LOCAL_NAME

echo "\n\033[0;32m*** SERVER SUCCEFULLY STARTED *** \033[1;37m"
echo '---------------------------------'
echo 'LOCAL_NAME\t'${LOCAL_NAME} 
echo 'LOCAL_IP\t'${LOCAL_IP} 
echo 'LOCAL_PORT\t'${LOCAL_PORT}
echo '---------------------------------\n'