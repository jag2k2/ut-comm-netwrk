from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class DumbellTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(4):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

def simpleTest():
    "Create and test a simple network"
    topo = DumbellTopo()
    net = Mininet(topo)
    net.start()

    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    host_addrs = dict({'h1': h1.IP(), 'h2': h2.IP(), 'h3': h3.IP(), 'h4': h4.IP()})
    popens = dict()
    
    print("Starting servers h2 and h4")
    popens[h2] = h2.popen('iperf3 -s -p 5566')
    popens[h4] = h4.popen('iperf3 -s -p 5566')
    
    print("Starting clients h1 and h3")
    popens[h1] = h1.popen('iperf3 -c {0} -p 5566 -i 1 -M 1460 -N -t 15 -y C > iperf_test_h1-h2_15s.txt'.format(h2.IP()), shell=True)
    popens[h3] = h3.popen('iperf3 -c {0} -p 5566 -i 1 -M 1460 -N -t 15 -y C > iperf_test_h3-h4_15s.txt'.format(h4.IP()), shell=True)
    popens[h1].wait()
    popens[h3].wait()

    popens[h2].terminate()
    popens[h4].terminate()
    popens[h2].wait()
    popens[h4].wait()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()