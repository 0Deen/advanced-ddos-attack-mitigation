from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class DDoSTopo(Topo):
    def build(self):
        # Add hosts and switch
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

def run():
    topo = DDoSTopo()
    # Define a RemoteController on localhost and port 6666
    controller = RemoteController('c0', ip='127.0.0.1', port=6666)
    net = Mininet(topo=topo, controller=lambda name: controller, link=TCLink)

    try:
        net.start()
        info("*** Dev 0Deen the Network has started\n")

        # Test connectivity
        info("*** Dev 0Deen , Testing connectivity\n")
        net.pingAll()

        # Launch CLI for interaction
        CLI(net)

    finally:
        info("*** Dev 0Deen Stopping network\n")
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class DDoSTopo(Topo):
    def build(self):
        # Add hosts and switch
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

def run():
    topo = DDoSTopo()
    # Define a RemoteController on localhost and port 6666
    controller = RemoteController('c0', ip='127.0.0.1', port=6666)
    net = Mininet(topo=topo, controller=lambda name: controller, link=TCLink)

    try:
        net.start()
        info("*** Dev 0Deen the Network started\n")

        # Test connectivity
        info("*** Dev 0Deen is Testing connectivity\n")
        net.pingAll()

        # Launch CLI for interaction
        CLI(net)

    finally:
        info("***Dev 0Deen the network in Stopping dummy\n")
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
