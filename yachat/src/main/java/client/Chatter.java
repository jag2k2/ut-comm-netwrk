package client;
import java.io.*; 
import java.net.*; 
import java.util.concurrent.*;
import common.Membership;
import common.Member;
import common.Command;

public class Chatter {
    public static void main(String[] args) throws Exception {
        if (args.length != 3) {
            System.out.println("ERROR: Provide 3 arguments");
            System.out.println("\t(1) <screenName>: Chatter's identity");
            System.out.println("\t(2) <hostAddress>: the address of the server");
            System.out.println("\t(3) <tcpPort>: the port number for TCP connection");
            System.exit(-1);
        }

        String myScreenName = args[0];
        String hostAddress = args[1];
        int tcpPort = Integer.parseInt(args[2]);
        String myIpAddress = InetAddress.getLocalHost().getHostAddress();

		Socket tcpSocket = new Socket(hostAddress, tcpPort); 
		DatagramSocket udpSocket = new DatagramSocket();
        int udpPort = udpSocket.getLocalPort();
        System.out.println("My Port is: " + udpPort);

		DataOutputStream outToServer = new DataOutputStream(tcpSocket.getOutputStream()); 
		BufferedReader inFromServer = new BufferedReader(new InputStreamReader(tcpSocket.getInputStream())); 

        String command = "HELO " + myScreenName + " " + myIpAddress + " " + udpPort + "\n";
        outToServer.writeBytes(command); 
        String tcpResponse;
        tcpResponse = inFromServer.readLine();
        Command tcpCommand = new Command(tcpResponse);

        if (tcpCommand.keywordMatches("ACPT")) {
            Membership membership = new Membership(tcpCommand.getPayload());
            System.out.println(membership.acceptMessage(myScreenName));
            Thread uiThread = new Thread(new UiHandler(outToServer, udpSocket));
            uiThread.start();
            while(true) {
                byte[] receiveData = new byte[1024];
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length); 
                udpSocket.receive(receivePacket);
                String udpResponse = new String(receivePacket.getData());
                Command udpCommand = new Command(udpResponse);
                if(udpCommand.keywordMatches("MESG")) {
                    System.out.println(udpCommand.getPayload());
                }
                if(udpCommand.keywordMatches("JOIN")) {
                    Member memberJoined = new Member(udpCommand.getPayload());
                    if (!memberJoined.screenName.equals(myScreenName)) {
                        membership.Add(memberJoined);
                        System.out.println(memberJoined.screenName + " has joined the chatroom");
                    }
                } 
                if(udpCommand.keywordMatches("EXIT")) {
                    String memberNameLeaving = udpCommand.getPayload();
                    if (!memberNameLeaving.equals(myScreenName)){
                        membership.Remove(memberNameLeaving);
                        System.out.println(memberNameLeaving + " has left the chatroom");
                    } else {
                        break;
                    }
                }
            }
            uiThread.interrupt();
        }
        else if (tcpCommand.keywordMatches("ACPT")) {
            System.out.println("Screen Name already exists: " + tcpCommand.getPayload());
        }
        else {
            System.out.println("Do not recoginze response: " + tcpResponse);
        }
        tcpSocket.shutdownOutput();
        tcpSocket.close();
        udpSocket.close();
        System.out.println("Client shutdown");
    }
}