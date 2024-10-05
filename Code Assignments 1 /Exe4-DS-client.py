import socket

def main():
    host = 'localhost'
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((host, port))
        
        while True:
            message = input("Message, or type 'end' to disconnect: ")
            server.sendall(message.encode('utf-8'))
            
            if message.lower() == "end":
                print("Disconnecting")
                break
            
            reply = server.recv(1024).decode('utf-8')
            print(f"Server said: {reply}")

if __name__ == "__main__":
    main()