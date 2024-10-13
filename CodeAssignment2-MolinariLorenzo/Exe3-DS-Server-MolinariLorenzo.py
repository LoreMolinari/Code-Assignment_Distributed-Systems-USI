import socket
from sys import argv
from threading import Thread
import message_exe3_pb2

n_users = 0
next_id = 1

def handle_client(conn, addr):
    global n_users, next_id
    with conn:
        print(f"Connected by {addr}")
        n_users += 1
        client_id = next_id
        next_id += 1

        handshake = message_exe3_pb2.Handshake()
        handshake.id = client_id
        handshake.error = False

        try:
            conn.sendall(handshake.SerializeToString())
        except Exception as e:
            print(f"Error handshake: {e}")
            n_users -= 1
            return

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message = message_exe3_pb2.Message()
                message.ParseFromString(data)
                print(f"Received from {message.sender} to {message.receiver}: {message.message}")

                conn.sendall(data)

                if message.message == "end":
                    break
        finally:
            n_users -= 1
        print(f"Closing connection, {addr}")

def operator():
    global n_users
    while True:
        command = input()
        if command == "num_users":
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