#!/bin/bash
sudo docker rm -f $(sudo docker ps -a -q --filter="name=mn." --format="{{.ID}}")