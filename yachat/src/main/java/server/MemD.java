package server;
import java.io.*;
import java.net.*;
import common.Membership;

public class MemD {
    public static void main (String[] args) throws IOException {
        int tcpPort;
        if (args.length != 1) {
            System.out.println("ERROR: Provide 1 arguments");
            System.out.println("\t(1) <tcpPort>: the port number for TCP connection");
            System.exit(-1);
        }
        tcpPort = Integer.parseInt(args[0]);

        System.out.println("Starting TCP server on port: " + tcpPort);
        try {
            ServerSocket listener = new ServerSocket(tcpPort);
            Socket clientConnection;
            DatagramSocket udpSocket = new DatagramSocket();
            Membership membership = new Membership();
            while ((clientConnection = listener.accept()) != null) {   
                Thread tcpHandlerThread = new Thread(new TcpHandler(clientConnection, udpSocket, membership));
                tcpHandlerThread.start();
            }
        } catch (IOException e){
            System.err.println("Server aborted: " + e.toString());
        }



        // try {
            // commandHandlerThread.join();//set up the critical section once and only once
            // udpListenerThread.join(); //set up the udpListener once and only once
            // tcpListenerThread.join(); //set up the tcpListener once and only once
        // } catch(InterruptedException err){
        //     System.out.println(err.toString());
        //     System.out.println("deleting all threads");
        // }
    }
}