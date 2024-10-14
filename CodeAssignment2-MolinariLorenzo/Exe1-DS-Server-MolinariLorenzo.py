import socket
from sys import argv
from threading import Thread, Lock

#users connected
n_users = 0
user_lock = Lock()

def handle_client(conn, addr):
    global n_users
    with conn:
        print(f"Connected by {addr}")
        with user_lock:
            n_users=n_users+1
        try:
            while True:
                data = conn.recv(1024)
                print(f"Received: {data.decode()}")
                if data == b"end":
                    break
                conn.sendall(data)
        finally:
            with user_lock:
                n_users=n_users-1
        print(f"Closing connection {addr}")

def operator():
    global n_users
    while True:
        command = input()
        if command == "num_users":
            with user_lock:
                print(f"Number of users: {n_users}")
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