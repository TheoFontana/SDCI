from mininet.net import Mininet
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

from functools import partial
net = Mininet()

import json
f =open('conf.json')
conf = json.load(f)
f.close()

def topology():
    
    info('*** Adding network controller\n')       
    c0 = net.addController(
        'c0',
        controller = RemoteController,
        p = '127.0.0.1',
        port = 6633 )

    info('*** Create final gateways\n')        
    fgs = [ 
        net.addDocker(  
            fg.local_name,
            ip = fg.locap_IP, 
            dimage = fg.image, 
            ports = fg.ports,
            port_bindings = fg.port_binding
        ) 
        for fg in conf.final_gateways
    ] 
    
    info('*** Create intermadiate gateways\n')
    ig = net.addDocker( 
        conf.gi.local_name,
        ip = conf.gi.locap_IP, 
        dimage = conf.gi.image, 
        ports = conf.gi.ports,
        port_bindings = conf.gi.port_binding
    ) 
    
    info('*** Create server\n')
    server = net.addDocker(     
        conf.server.local_name,
        ip = conf.server.locap_IP, 
        dimage = conf.server.image, 
        ports = conf.server.ports,
        port_bindings = conf.server.port_binding
    ) 
    
    info('*** Create data center\n')
    data_center = net.addDocker(    
        conf.server.local_name,
        ip = conf.server.locap_IP, 
        dimage = conf.server.image, 
        ports = conf.server.ports,
        port_bindings = conf.server.port_binding
    )
    info('*** Create switchs\n')
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )

    info('*** Create network links\n')
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s1, s3 )

    for fg in fgs :
        net.addLink( fg, s2 )
        
    net.addLink( ig, s1 )
    net.addLink( server, s1 )
    net.addLink( data_center, s3 )

    info('***  Start network\n')
    net.start()
    info('***  Running CLI\n')
    CLI( net )
    info('***  Stop network\n')
    net.stop()

if __name__ == "__main__" :
    setLogLevel('info')
    topology()