# ECE381K YaChat - A Chat System
This repo includes a chatter client application that implements the YaChat Chatroom protocol system.

## How to Build and Run the Project

- cd to `../yachat`
- `mkdir bin`
- `javac -d bin src/main/java/**/*.java`
- `cd bin`
- `jar cf YaChat.jar **/*.class`
- `java -cp YaChat.jar server.MemD <tcp-port>`
- `java -cp YaChat.jar client.Chatter <screen-name> <address> <tcp-port>`
