#!/bin/sh

sudo docker rm $(docker stop $(docker ps -a -q --filter="name=dev-" --format="{{.ID}}"))
sudo docker rmi $(sudo docker images theofontana/device -q) -f
