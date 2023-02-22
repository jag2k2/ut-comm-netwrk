package server;
import java.io.*;
import java.net.*;
import java.util.NoSuchElementException;
import java.util.Scanner;
import common.Command;
import common.Membership;
import common.Member;

public class TcpHandler implements Runnable{
    Socket clientConnection;
    DatagramSocket udpSocket;
    Membership membership;
    String clientName;

    public TcpHandler(Socket clientConnection, DatagramSocket udpSocket, Membership membership) {
        this.clientConnection = clientConnection;
        this.udpSocket = udpSocket;
        this.membership = membership;
        this.clientName = "";
    }

    @Override
    public void run() {
        try {
            Scanner commandScanner = new Scanner(clientConnection.getInputStream());
            PrintWriter responseWriter = new PrintWriter(clientConnection.getOutputStream());
            while(true){
                try {
                    String clientCommand = commandScanner.nextLine();
                    Command command = new Command(clientCommand);
                    if (command.keywordMatches("HELO")){
                        Member newMember = new Member(command.getPayload());
                        String response = "";
                        if (membership.ScreenNameExists(newMember.screenName)){
                            response = "RJCT " + newMember.screenName + "\n";
                            responseWriter.print(response);
                            responseWriter.flush();
                            clientConnection.close();
                            break;
                        }
                        else{
                            clientName = newMember.screenName;
                            membership.Add(newMember);
                            response = "ACPT " + membership.toString() + "\n";
                            responseWriter.print(response);
                            responseWriter.flush();
                            String joinCommand = "JOIN " + newMember.screenName + " " + newMember.ipAddress + " " + Integer.toString(newMember.udpPort) + "\n";
                            membership.Send(joinCommand, udpSocket);
                        } 
                    }
                    else if (command.keywordMatches("EXIT")){
                        String exitCommand = "EXIT " + clientName + "\n";
                        membership.Send(exitCommand, udpSocket);
                        clientConnection.close();
                        membership.Remove(clientName);
                        break;
                    }
                } catch (NoSuchElementException e) {
                    String exitCommand = "EXIT " + clientName + "\n";
                    membership.Send(exitCommand, udpSocket);
                    membership.Remove(clientName);
                    break;
                }
            }
        } catch (IOException e){
            System.err.print(e);
        }
    }
}
