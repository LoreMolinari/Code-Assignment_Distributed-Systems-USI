import socket
from sys import argv
import Exe1_pb2
from threading import Thread


def send_message(conn, m):
    serialized = m.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
    conn.sendall(serialized)


def receive_message(conn, m):
    msg = m()
    size = int.from_bytes(conn.recv(4), byteorder="big")
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg


def main():
    host = "127.0.0.1"
    port = None
    try:
        if len(argv) > 2:
            host = argv[1]
            port = int(argv[2])
        elif len(argv) > 1:
            port = int(argv[1])
        else:
            raise ValueError
    except:
        host = host or "127.0.0.1"
        port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")

        handshake = receive_message(s, Exe1_pb2.FastHandshake)
        if handshake.error:
            print("Server rejected the connection")
            return

        print(f"Client started with ID: {handshake.id}")
        id = handshake.id

        Thread(target=handle_incoming_messages,args=(s,), daemon=True).start()
        
        while True:
            try:
                user_input = input("Enter message in format [id] [message]: \n")
                target_id_str, msg_text = user_input.split(" ", 1)
                target_id = int(target_id_str)
                    
                msg = Exe1_pb2.Message(fr=id, to=target_id, msg=msg_text)
                send_message(s, msg)
            except ValueError:
                print("Errore: invalid input format. Use [id] [message].\n")
                continue
        
        print("Closing connection")


def handle_incoming_messages(conn):
    print('waiting for messages...')
    while True:
        msg = receive_message(conn, Exe1_pb2.Message)
        print(f"Message received: {msg.msg}, from client: {msg.fr}")

if __name__ == "__main__":
    main()

