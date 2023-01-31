package client;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramSocket;

public class UiHandler implements Runnable{

    private DataOutputStream outToServer;
    private DatagramSocket udpSocket;

    public UiHandler(DataOutputStream outToServer, DatagramSocket udpSocket){
        this.outToServer = outToServer;
        this.udpSocket = udpSocket;
    }

    @Override
    public void run() {
        BufferedReader userReader = new BufferedReader(new InputStreamReader(System.in));
        while (!Thread.interrupted()) { 
            String userCommand = null;
            try {
                userCommand = userReader.readLine();
                if (userCommand == null) {
                    String command = "EXIT\n";
                    outToServer.writeBytes(command);
                    break; 
                } else {
                    //String command = ""
                }
            } catch (IOException err) {
                System.out.println(err.toString());
            }
        }
    }
}
