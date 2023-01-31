package common;
import java.lang.Integer;

public class Member {
    public String screenName;
    public String ipAddress;
    public int udpPort;

    public Member(String memberString) {
        String[] tokens = memberString.split(" ");
        this.screenName = tokens[0];
        this.ipAddress = tokens[1];
        this.udpPort = Integer.parseInt(tokens[2]);
    }

    public boolean nameEquals(String name) {
        return (this.screenName.equals(name));
    }
}