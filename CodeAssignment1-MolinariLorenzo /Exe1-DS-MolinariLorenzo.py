import socket
from sys import argv

def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    print(f"Server started on port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("Waiting for a client...")

        # Accept the connection to the client
        conn, addr = s.accept()  
        with conn:
            print(f"Connected by {addr}")
            
            message = conn.recv(1024).decode('utf-8')
            print(f"Message received: {message}")

        # Close the connection to the client
        print("Closing connection")

if __name__ == "__main__":
    main()
