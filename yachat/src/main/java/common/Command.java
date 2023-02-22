package common;

public class Command {
    private String keyword = "";
    private String payload = "";

    public Command(String raw_command){
        String[] newLineTokens = raw_command.split("\n");
        String[] tokens = newLineTokens[0].split(" ", 2);
        this.keyword = tokens[0];
        if (tokens.length > 1){
            this.payload = tokens[1];
        }
    }

    public boolean keywordMatches(String keyword) {
        return this.keyword.contains(keyword);
    }

    public String getPayload() {
        return this.payload;
    }
}
