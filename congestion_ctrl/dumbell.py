from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

class DumbellTopo(Topo):
    def build(self, delay=2):
        """ Create the topology by overriding the class parent's method.
            :param  delay   One way propagation delay, delay = RTT / 2. Default is 2ms.
        """
        # The bandwidth (bw) is in Mbps, delay in milliseconds and queue size is in packets
        backbone_params = dict(bw=984, delay='{0}ms'.format(delay), max_queue_size=82*delay, use_htb=True)  # backbone router interface tc params
        access_params = dict(bw=252, delay='0ms', max_queue_size=(21*delay*20)/100, use_htb=True)  # access router intf tc params
        # TODO: remove queue size from hosts and try.
        host_params = dict(bw=960, delay='0ms', max_queue_size=80*delay, use_htb=True)  # host interface tc params

        backbone_switch1 = self.addSwitch('bs1')
        backbone_switch2 = self.addSwitch('bs2')
        access_switch1 = self.addSwitch('as1')
        access_switch2 = self.addSwitch('as2')

        # Link backbone switches
        self.addLink(backbone_switch1, backbone_switch2, cls=TCLink, **backbone_params)

        # Link access switches to the backbone switches
        self.addLink(backbone_switch1, access_switch1, cls=TCLink, **access_params)
        self.addLink(backbone_switch2, access_switch2, cls=TCLink, **access_params)

        # Create senders and receivers
        source1 = self.addHost('src1')
        source2 = self.addHost('src2')
        receiver1 = self.addHost('rcv1')
        receiver2 = self.addHost('rcv2')

        # Link the senders to Access Switch 1
        self.addLink(access_switch1, source1, cls=TCLink, **host_params)
        self.addLink(access_switch1, source2, cls=TCLink, **host_params)

        # Link the receivers to Access Switch 2
        self.addLink(access_switch2, receiver1, cls=TCLink, **host_params)
        self.addLink(access_switch2, receiver2, cls=TCLink, **host_params)

def commTest():
    topo = DumbellTopo()
    net = Mininet(topo)
    net.start()

    source1, source2, receiver1, receiver2 = net.get('src1', 'src2', 'rcv1', 'rcv2')
    popens = dict()
    print("Starting receivers")
    popens[receiver1] = receiver1.popen('iperf3 -s -p 5566')
    popens[receiver2] = receiver2.popen('iperf3 -s -p 5566')
    
    print("Starting senders")
    popens[source1] = source1.popen('iperf3 -c {0} -p 5566 -i 1 -M 1460 -N -t 15 > iperf_test_h1-h2_15s.txt'.format(h2.IP()), shell=True)
    popens[source2] = source2.popen('iperf3 -c {0} -p 5566 -i 1 -M 1460 -N -t 15 > iperf_test_h3-h4_15s.txt'.format(h4.IP()), shell=True)
    popens[source1].wait()
    popens[source2].wait()

    popens[receiver1].terminate()
    popens[receiver2].terminate()
    popens[receiver1].wait()
    popens[receiver2].wait()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    commTest()