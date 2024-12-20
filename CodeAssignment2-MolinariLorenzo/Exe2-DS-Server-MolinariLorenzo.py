import socket
from sys import argv
from threading import Thread, Lock
import message_exe2_pb2  # Import file protoc

n_users = 0
n_users_lock = Lock()

def handle_client(conn, addr):
    global n_users
    with conn:
        print(f"Connected by {addr}")
        with n_users_lock:
            n_users=n_users+1
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message = message_exe2_pb2.Message()
                message.ParseFromString(data)
                print(f"Message from {message.sender} to {message.receiver}: {message.message}")

                conn.sendall(data)

                if message.message == "end":
                    break
        finally:
            with n_users_lock:
                n_users=n_users-1
        print(f"Closing connection to {addr}")

def operator():
    global n_users
    while True:
        command = input()
        if command == "num_users":
            with n_users_lock:
                print(f"Users: {n_users}")
        elif command == "quit":
            print("Shut down operator")
            break

def main():
    global n_users
    try:
        port = int(argv[1])
    except:
        port = 8080

    t_operator = Thread(target=operator, daemon=True)
    t_operator.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        print(f"Server started on port {port}")
        print("Waiting for a client...")
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr)).start()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()