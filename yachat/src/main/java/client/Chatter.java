import java.util.Scanner;

public class Chatter {
    public static void main(String[] args) {
        String screenName;
        String hostAddress;
        int tcpPort;
        
        int udpPort;

        if (args.length != 3) {
            System.out.println("ERROR: Provide 3 arguments");
            System.out.println("\t(1) <screenName>: Chatter's identity");
            System.out.println("\t(2) <hostAddress>: the address of the server");
            System.out.println("\t(3) <tcpPort>: the port number for TCP connection");
            System.exit(-1);
        }

        screenName = args[0];
        hostAddress = args[1];
        tcpPort = Integer.parseInt(args[2]);

        // CanCommunicate connection = new TcpConnection(hostAddress, tcpPort);
        // CanShop shopper = new Shopper(connection);

        Scanner sc = new Scanner(System.in);
        while (sc.hasNextLine()) {
            String cmd = sc.nextLine();
            String[] tokens = cmd.split(" ");
            System.out.println(cmd);
        }
        System.out.println("goodbye!");
    }
}