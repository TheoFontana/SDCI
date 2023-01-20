# Copyright (c) 2015 SONATA-NFV and Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
import logging
from mininet.log import setLogLevel
from emuvim.dcemulator.net import DCNetwork
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

import json
import requests


logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)

metadata_srv_URL= 'http://metadata_server/'

def create_topology():
    net = DCNetwork(monitor=False, enable_learning=True)

    dc1 = net.addDatacenter("dc1")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.start()

    info('*** Creating server ***\n')
    srv_r = requests.get(url = metadata_srv_URL+'srv')
    srv_conf = srv_r.json()
    server = net.addDocker(
        srv_conf['local_name'],
        ip = srv_conf['local_ip'],
        dimage = 'theofontana/server:2.0',
        environment ={"INSTANCE_ID":srv_conf['local_name']}
    )

    info('*** Creating intermediate gateway ***\n')
    gwi_r = requests.get(url = metadata_srv_URL+'gwi')
    gwi_conf = gwi_r.json()
    gwi =net.addDocker(
        gwi_conf['local_name'],
        ip = gwi_conf['local_ip'],
        dimage = 'theofontana/gateway:2.0',
        environment ={"INSTANCE_ID":gwi_conf['local_name']}
    )
    info('*** Creating finals gateways ***\n')
    gwfs=[]
    for i in range (1,4):
        gw_r = requests.get(url = metadata_srv_URL+'gwf_'+str(i))
        gw_conf = gw_r.json()
        gwf =net.addDocker(
            gw_conf['local_name'],
            ip = gw_conf['local_ip'],
            dimage = 'theofontana/gateway:2.0',
            environment ={"INSTANCE_ID":gw_conf['local_name']}
        )
        gwfs.append(gwf)

    info('*** Creating devices ***\n')
    devices=[]
    for i in range (1,10):
        dev_r = requests.get(url = metadata_srv_URL+'dev_'+str(i))
        dev_conf = dev_r.json()
        dev = net.addDocker(
            dev_conf['local_name'],
            ip = dev_conf['local_ip'],
            dimage = 'theofontana/device:2.0',
            environment ={"INSTANCE_ID":dev_conf['local_name']}
        )
        devices.append(dev)

    info('*** Adding switches ***\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info('*** Creating links\n')
    for gwf in gwfs :
        net.addLink(s3, gwf)

    for dev in devices[0:3]:
        net.addLink(gwfs[0], dev)
    for dev in devices[3:6]:
        net.addLink(gwfs[1], dev)
    for dev in devices[6:9]:
        net.addLink(gwfs[2], dev)

    net.addLink(s1, gwi)
    net.addLink(gwi, s1)
    net.addLink(s1, server)
    net.addLink(s2, dc1)
    net.addLink(s1, s2)
    net.addLink(s1, s3)

    net.start()
    net.CLI()
    # when the user types exit in the CLI, we stop the emulator
    net.stop()


def main():
    create_topology()


if __name__ == '__main__':
    main()