#! /bin/sh

for i in dv1 dv2 dv3 dv4 dv5 dv6 dv7 dv8 dv9
do
    sudo docker build --network host --build-arg GW_ID=$i -t theofontana/gateway:$i .
done