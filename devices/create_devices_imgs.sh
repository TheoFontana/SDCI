#! /bin/sh

i=0
while [ $i -ne 9 ]
do
    i=$(($i+1))
    sudo docker build --network host --build-arg DV_ID=dev-$i -t theofontana/device:dev-$i .
done