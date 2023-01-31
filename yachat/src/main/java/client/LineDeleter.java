package client;

public class LineDeleter {
    static public void DeleteLastLine(){
        System.out.print(String.format("\033[%dA", 1));     // Move up
        System.out.print("\033[2K");                        // Erase line content
    }
}
