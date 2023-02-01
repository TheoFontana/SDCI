#!/usr/bin/env python3

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
import os
# import pdb; pdb.set_trace()

monitoring = True
delay_monitoring = 5
delay_start=5

#execute vim emu
def start_monitoring():
    # URL to add new vnf
    url = 'http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitor'
    headers = {'Content-type': 'application/json'}
    d = {"image":"vnf_monitor:0.2", "network":"(id=vnf_monitor,ip=10.1.0.100/24)"}
    r = requests.put(url, headers=headers, data = json.dumps(d))
    return r.status_code, r.json()

def create_gwi():
    # Making a PUT request
    url = 'http://127.0.0.1:5001/restapi/compute/dc1/vnf_gwi'
    headers = {'Content-type': 'application/json'}
    d = {"image":"vnf_gwi_dc:0.1", "network":"(id=vnf_gwi,ip=10.1.0.60/24)"}
    r = requests.put(url, headers=headers, data = json.dumps(d))
    return r.status_code, r.json()

def monitor_gwi(add_gwi, port_gwi):
    # Making a GET request
    url = "http://"+ str(add_gwi)+":"+str(port_gwi)+"/monitor"
    r = requests.get(url)
    return r.status_code, r.json()

#Modification of destination gwi 1 to gwi 2 (nfv)
def traffic_redirection(nw_src, nw_dst, ipv4_dst):
    # URL of SDN Controller
    url = 'http://127.0.0.1:8080/stats/flowentry/add'
    d = {
        "dpid": 2,
        "table_id":0,
        "priority":11111,
        "match":{
            "nw_src": nw_src,
            "nw_dst": nw_dst,
            "dl_type": "2048",
        },
        "actions":[
                {
                    "type": "SET_FIELD",
                    "field": "ipv4_dst",
                    "value": ipv4_dst
                },
                {
                    "type": "OUTPUT",
                    "port": "NORMAL"
                }
            ]
        }
    # r = requests.post(url, data = str(d))
    os.system("sh redirect_gwi_to_vnf.sh")
    os.system("sudo curl -X GET http://localhost:8080/stats/flow/2 > rule1.json")
    d = {
        "dpid": 2,
        "table_id":0,
        "priority":11111,
        "match":{
            "nw_src": ipv4_dst,
            "nw_dst": nw_src,
            "dl_type": "2048",
        },
        "actions":[
                {
                    "type": "SET_FIELD",
                    "field": "ipv4_dst",
                    "value": nw_dst
                },
                {
                    "type": "OUTPUT",
                    "port": "NORMAL"
                }
            ]
        }
    # r = requests.post(url, data = str(d))
    os.system("sh redirect_vnf_from_gwi.sh")
    os.system("sudo curl -X GET http://localhost:8080/stats/flow/2 > rule2.json")
    return 200


if __name__ == '__main__':
    code_monitoring, resp = start_monitoring()
    while(code_monitoring != 200):
        try:
            time.sleep(delay_start)
            start, resp = start_monitoring()
        except:
            print("Error starting the monitoring", code_monitoring)
            continue

    single_gwi = True
    docker_network = resp["docker_network"]
    print("docker_network ", docker_network)
    while(monitoring):
        time.sleep(delay_monitoring)
        try:
            code_monitor_gwi, resp_monitor = monitor_gwi(docker_network, "8888")
            if(code_monitor_gwi >= 400):
                raise Exception("Error monitoring")
            else:
                #get traffic info
                print("avgLoad", resp_monitor["avgLoad"])
                print("currentLoadSystem", resp_monitor["currentLoadSystem"])
                if(resp_monitor["currentLoadSystem"] > 5):
                    traffic_issue = True
                else:
                    traffic_issue = False
                if(traffic_issue and single_gwi):
                    try:
                        code_gwi, resp_gwi = create_gwi()
                        print("code_gwi ", code_gwi)
                        print("resp_gwi ", resp_gwi)
                        if (code_gwi == 200):
                            single_gwi = False
                            vnf_gwi_ip = resp_gwi["network"][0]["ip"]
                            print("vnf_gwi_ip ", vnf_gwi_ip)
                            vnf_gwi_ip=vnf_gwi_ip.replace("/24","")
                            print("vnf_gwi_ip ", vnf_gwi_ip)
                            code_traffic_redirection = traffic_redirection(nw_src="10.1.0.11",nw_dst="10.1.0.10",ipv4_dst=vnf_gwi_ip)
                            print("code_traffic_redirection ", code_traffic_redirection)
                            # input("Verify the rules...")
                            continue
                    except:
                        print("", code_gwi, code_traffic_redirection)
                        continue
        except:
            print("Connection refused by the monitor_gwi")
            continue