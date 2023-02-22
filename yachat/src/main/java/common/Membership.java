package common;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Membership {
    private ConcurrentLinkedQueue<Member> members = new ConcurrentLinkedQueue<>();

    public Membership(String membership_string) {
        String[] member_strings = membership_string.split(":");
        for (String memberString : member_strings) {
            Member member = new Member(memberString);
            members.add(member);
        }
    }

    public Membership() {}

    public void Add(Member member) {
        members.add(member);
    }

    public boolean ScreenNameExists(String screenName){
        for (Member member : members){
            if (member.nameEquals(screenName)){
                return true;
            }
        }
        return false;
    }

    public void Remove(String memberName) {
        members.removeIf(n -> (n.nameEquals(memberName)));
    }

    public void Send(String command, DatagramSocket udpSocket) throws IOException {
        for (Member member : members) {
            byte[] sendData = new byte[1024]; 
            sendData = command.getBytes();
            InetAddress memberAddress = InetAddress.getByName(member.ipAddress);
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, memberAddress, member.udpPort);
            udpSocket.send(sendPacket);
        }
    }

    public String acceptMessage(String myName) {
        String acceptString = "";
        String chatroomMsg = " is in the chatroom\n";
        String acceptMsg = " accepted to the chatroom\n";
        for(Member member : members) {
            if (member.screenName.equals(myName)) {
                acceptString += member.screenName + acceptMsg;
            } else {
                acceptString += member.screenName + chatroomMsg;
            }
        }
        return acceptString;
    }

    @Override
    public String toString() {
        String membershipString = "";
        for (Member member : members) {
            membershipString += member.screenName + " " + member.ipAddress + " " + Integer.toString(member.udpPort) + ":";
        }
        int delimPosition = membershipString.lastIndexOf(':');
        if (delimPosition >= 0){
            membershipString = membershipString.substring(0, delimPosition);
        }
        return membershipString;
    }
}
