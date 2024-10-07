import socket

def main():
    server = '127.0.0.1'
    port = 8080

    user_input = input("Enter a message to send: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((server, port))
            print(f"Connected server {server}:{port}")
            
            s.sendall(user_input.encode('utf-8'))

            reply = s.recv(1024).decode('utf-8')
            print(f"Reply: {reply}")

        except ConnectionRefusedError:
            print("Error, server connection. Make sure the server is running.")

if __name__ == "__main__":
    main()
