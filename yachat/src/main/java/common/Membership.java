package common;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Membership {
    private ConcurrentLinkedQueue<Member> members;

    public Membership(String[] member_strings) {
        this.members = new ConcurrentLinkedQueue<>();
        for (String memberString : member_strings) {
            String[] tokens = memberString.split(" ");
            Member member = new Member(tokens[0], tokens[1], Integer.parseInt(tokens[2]));
            members.add(member);
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
            membershipString += member.screenName + " " + member.ipAddress + " " + Integer.toString(member.udpPort) + "\n";
        }
        return membershipString;
    }
}
