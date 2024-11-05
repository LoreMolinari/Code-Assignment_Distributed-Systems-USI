import socket
from sys import argv
import Exe2_pb2
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
    host = None
    port = None
    try:
        if len(argv) == 2:
            new_id = int(argv[1])
            host = host or "127.0.0.1"
            port = 8080
        elif len(argv) == 3:
            host = argv[1]
            port = int(argv[2])
            new_id = None
        elif len(argv) == 4:
            host = argv[1]
            port = int(argv[2])
            new_id = int(argv[3])
        else:
            raise ValueError("Invalid arguments")
    except:
        host = host or "127.0.0.1"
        port = 8080
        new_id = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")
        
        if new_id:
            handshake = Exe2_pb2.Handshake(ID=new_id,newID = True)
            send_message(s, handshake)
        else:
            handshake = Exe2_pb2.Handshake(newID = False)
            send_message(s, handshake)
        
        handshake = receive_message(s, Exe2_pb2.Handshake)
        
        if handshake.newID:
            print('new id accepted!')
            print(f"id: {handshake.ID}")
        else:
            print(f"id created: {handshake.ID}")
        
        id = handshake.ID
            
        if handshake.error:
            print(f"Handshake failed")
            return

        Thread(target=handle_incoming_messages,args=(s,), daemon=True).start()
        
        while True:
            try:
                user_input = input("Enter message in format [id] [message]: \n")
                target_id_str, msg_text = user_input.split(" ", 1)
                target_id = int(target_id_str)
                    
                msg = Exe2_pb2.Message(fr=id, to=target_id, msg=msg_text)
                send_message(s, msg)
            except ValueError:
                print("Errore: invalid input format. Use [id] [message].\n")
                continue
        
        print("Closing connection")


def handle_incoming_messages(conn):
    while True:
        msg = receive_message(conn, Exe2_pb2.Message)
        print(f"New message: {msg.msg} from client {msg.fr}")

if __name__ == "__main__":
    main()

