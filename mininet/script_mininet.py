from mininet.net import Mininet
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from functools import partial
import json
import requests

net = Containernet(controller=Controller)

metadata_srv_URL= 'http://metadata_server/'

def topology():
    info('*** Adding network controller ***\n')
    info('*** Create server ***\n')
    
    srv_r = requests.get(url = metadata_srv_URL+'srv')
    srv_conf = srv_r.json()

    gwi_r = requests.get(url = metadata_srv_URL+'srv')
    gwi_conf = gwi_r.json()
    
    server = net.addDocker(
        srv_conf['local_name'],
        ip = srv_conf['local_IP'],
        dimage = 'theofontana/server'
    )

    gwi =net.addDocker(
        gwi_conf['local_name'],
        ip = gwi_conf['local_IP'],
        dimage = 'theofontana/gateway:gwi'
    )

    info('*** Start network ***\n')
    net.start()
    info('*** Running CLI ***\n')
    CLI( net )
    info('*** Stop network ***\n')
    net.stop()

if __name__ == "__main__" :
   setLogLevel('info')
   topology()