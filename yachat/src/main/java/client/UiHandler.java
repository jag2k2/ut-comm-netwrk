package client;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramSocket;
import common.Membership;

public class UiHandler implements Runnable{

    private DataOutputStream outToServer;
    private DatagramSocket udpSocket;
    private String myScreenName;
    private Membership membership;

    public UiHandler(DataOutputStream outToServer, DatagramSocket udpSocket, String myScreenName, Membership membership){
        this.outToServer = outToServer;
        this.udpSocket = udpSocket;
        this.myScreenName = myScreenName;
        this.membership = membership;
    }

    @Override
    public void run() {
        BufferedReader userReader = new BufferedReader(new InputStreamReader(System.in));
        while (!Thread.interrupted()) { 
            String userComment = null;
            try {
                userComment = userReader.readLine();
                if (userComment == null) {
                    String command = "EXIT\n";
                    outToServer.writeBytes(command);
                    break; 
                } else {
                    String command = "MESG " + myScreenName + ": " + userComment + "\n";
                    membership.Send(command, udpSocket);
                }
            } catch (IOException err) {
                System.out.println(err.toString());
            }
        }
    }
}
