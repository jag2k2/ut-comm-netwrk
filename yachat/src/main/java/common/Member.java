package common;

public class Member {
    public String screenName;
    public String ipAddress;
    public int udpPort;

    public Member(String screenName, String ipAddress, int udpPort) {
        this.screenName = screenName;
        this.ipAddress = ipAddress;
        this.udpPort = udpPort;
    }
}