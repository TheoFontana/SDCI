#!/bin/sh

i=0
while [ $i -ne 1 ]
do
    i=$(($i+1))
    sudo docker build --network host --build-arg APP_ID=app-$i -t theofontana/app:app-$i .
done
