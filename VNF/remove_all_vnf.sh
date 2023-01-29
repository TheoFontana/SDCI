# !/bin/sh

sudo docker rm -f $(sudo docker ps -a -q --filter="name=vnf_" --format="{{.ID}}")