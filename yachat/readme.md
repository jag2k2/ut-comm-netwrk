# ECE381K YaChat - A Chat System
This repo includes both a server and client application that implements the YaChat Chatroom system.

## Table of Contents:
1. [Project Specification](#project-specification)
2. [How to Build and Run the Project](#how-to-build-and-run-the-project)
3. [Contributors](#contributors)

## Project Specification

The following commands may be issued by the client

- **HELO <screen_name> <IP> <Port>\n**
- **MESG <screen_name>: <message>\n**
- **EXIT\n**

## How to Build and Run the Project

- cd to `../yachat`
- `mkdir bin`
- `javac -d bin src/main/java/**/*.java`
- `cd bin`
- `jar cf YaChat.jar **/*.class`
- `java -cp YaChat.jar client.Chatter <screen-name> <address> <tcp-port>`
- `java -cp YaChat.jar server.Server`

## Contributors
- [Jeff Tipps](https://github.com/jag2k2) jt45679
