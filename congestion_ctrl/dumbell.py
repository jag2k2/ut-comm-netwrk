from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

class DumbellTopo(Topo):
    def build(self, delay=0):
        # The bandwidth (bw) is in Mbps, delay in milliseconds and queue size is in packets
        packet_size = 1500
        bits = 8

        backbone_speed = 82
        backbone_bandwidth = backbone_speed * packet_size * 1000 * bits / 1000000
        backbone_params = dict(bw=backbone_bandwidth, delay='{0}ms'.format(delay), max_queue_size=backbone_speed*delay, use_htb=True)
        
        access_speed = 21
        access_bandwidth = access_speed * packet_size * 1000 * bits / 1000000
        access_params = dict(bw=access_bandwidth, delay='0ms', max_queue_size=(0.2*access_speed*delay), use_htb=True)
        
        host_speed = 80
        host_bandwidth = host_speed * packet_size * 1000 * bits / 1000000
        host_params = dict(bw=host_bandwidth, delay='0ms', max_queue_size=host_speed*delay, use_htb=True)

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

def commTest(delay=2):
    topo = DumbellTopo(delay=delay)
    net = Mininet(topo)
    net.start()

    source1, source2, receiver1, receiver2 = net.get('src1', 'src2', 'rcv1', 'rcv2')
    popens = dict()
    print("Starting receivers")
    popens[receiver1] = receiver1.popen('iperf3 -s -p 5566')
    popens[receiver2] = receiver2.popen('iperf3 -s -p 5566')
    
    print("Starting Flow 1")
    # popens[source1] = source1.popen('iperf3 -c {0} -p 5566 -i 1 -C cubic -t 200 > iperf3_data_flow1_{1}_{2}.txt'.format(receiver1.IP(), 'default', delay), shell=True)
    popens[source1] = source1.popen('iperf3 -c {0} -p 5566 -V -4 -i 1 -C cubic -f m -d -t 20 > iperf3_data_flow1_{1}_{2}.txt'.format(receiver1.IP(), 'default', delay), shell=True)

    print("Delaying Flow 2")
    sleep(10)

    print("Starting Flow 2")
    # popens[source2] = source2.popen('iperf3 -c {0} -p 5566 -i 1 -C cubic -t 100 > iperf3_data_flow2_{1}_{2}.txt'.format(receiver2.IP(), 'default', delay), shell=True)
    popens[source2] = source2.popen('iperf3 -c {0} -p 5566 -V -4 -i 1 -C cubic -f m -d -t 10 > iperf3_data_flow2_{1}_{2}.txt'.format(receiver2.IP(), 'default', delay), shell=True)
    popens[source1].wait()
    popens[source2].wait()

    popens[receiver1].terminate()
    popens[receiver2].terminate()
    popens[receiver1].wait()
    popens[receiver2].wait()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    commTest(21)