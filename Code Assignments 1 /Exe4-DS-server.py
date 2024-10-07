import socket
import threading
from sys import argv


def clientConnection(conn, addr):
    print(f"Host {addr} connected")
    
    while True:
        message = conn.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"host {addr} said: {message}")
        
        if message.lower() == "end":
            print(f"Client {addr} disconnected.")
            break
        
        reply_message = "Message correctly received"
        conn.sendall(reply_message.encode('utf-8'))
    
    conn.close()

def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    print(f"Server on port: {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:    
        client.bind(("0.0.0.0", port))
        client.listen()
        print("Connection open to clients...")

        while True:
            conn, addr = client.accept()
            client_thread = threading.Thread(target=clientConnection, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()