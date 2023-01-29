# !/bin/sh

sudo docker build -t vnf_monitor:0.2 --network host .
#sudo docker run -e ENV_ADD_GWI=10.1.0.10 -e ENV_PORT_GWI=8181 -d --name vnf_monitor vnf_monitor:0.1