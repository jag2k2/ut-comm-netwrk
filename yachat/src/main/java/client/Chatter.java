package client;
import java.io.*; 
import java.net.*; 

public class Chatter {
    public static void main(String[] args) throws Exception {
        
        if (args.length != 3) {
            System.out.println("ERROR: Provide 3 arguments");
            System.out.println("\t(1) <screenName>: Chatter's identity");
            System.out.println("\t(2) <hostAddress>: the address of the server");
            System.out.println("\t(3) <tcpPort>: the port number for TCP connection");
            System.exit(-1);
        }

        String screenName = args[0];
        String hostAddress = args[1];
        int tcpPort = Integer.parseInt(args[2]);
        String myIpAddress = InetAddress.getLocalHost().getHostAddress();

        // CanCommunicate connection = new TcpConnection(hostAddress, tcpPort);
        // CanShop shopper = new Shopper(connection);

		// BufferedReader inFromUser = 
		// 	new BufferedReader(new InputStreamReader(System.in)); 

		Socket tcpSocket = new Socket(hostAddress, tcpPort); 
		DatagramSocket udpSocket = new DatagramSocket();
        int udpPort = udpSocket.getLocalPort();
        System.out.println("My Port is: " + udpPort);

		DataOutputStream outToServer = new DataOutputStream(tcpSocket.getOutputStream()); 
		BufferedReader inFromServer = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream())); 

        String command = "HELO " + screenName + " " + myIpAddress + " " + udpPort + "\n";
        System.out.println(command);
        outToServer.writeBytes(command); 
        String response;
        while ((response = inFromServer.readLine()) != null) { 
			
			System.out.println("FROM SERVER: " + response); 
		}
        tcpSocket.close();
        udpSocket.close();
        System.out.println("goodbye!");
    }
}