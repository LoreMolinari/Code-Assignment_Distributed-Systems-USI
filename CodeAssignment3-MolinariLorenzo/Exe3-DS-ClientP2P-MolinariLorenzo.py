import socket
import threading
import snowflake
from Exe3_pb2 import Message
import sys

ASSIGNER_ID = 7043770
peers = []
received_messages = set()

# Rewrote most of the server and client code from previous exercise
# I assumend that exercise works in broadcast way, since when peers are passed we don't pass the ID

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peer_id = snowflake.derive_id(ASSIGNER_ID)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        print(f"Assigned ID: {self.peer_id}, client: {self.host}:{self.port}")

    def add_peer(self, peer_host, peer_port):
        peers.append((peer_host, peer_port))
        print(f"Peer added with address {peer_host}:{peer_port}")

    def send_message(self, message):
        for peer_addr in peers:
            self.sock.sendto(message.SerializeToString(), peer_addr)
            print(f"\nBroadcasting message to {peer_addr}")

    def listen_for_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = Message()
            message.ParseFromString(data)

            msg_id = (message.fr, message.msg)

            if msg_id in received_messages:
                continue
            received_messages.add(msg_id)

            if message.to == self.peer_id:
                print(f"\nReceived message from {message.fr}: {message.msg}")
                if message.msg != "Ack":
                    confirm_msg = Message()
                    confirm_msg.fr = self.peer_id
                    confirm_msg.to = message.fr
                    confirm_msg.msg = "Ack"
                    self.sock.sendto(confirm_msg.SerializeToString(), addr)
            else:
                if message.msg != "Ack":
                    self.send_message(message)

    def run(self):
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True
        listener_thread.start()

        while True:
            try:
                user_input = input("Enter message in format [id] [message]: \n")
                target_id_str, msg_text = user_input.split(" ", 1)
                target_id = int(target_id_str)

                msg = Message()
                msg.fr = self.peer_id
                msg.to = target_id
                msg.msg = msg_text
                self.send_message(msg)
            except ValueError:
                print("Errore: invalid input format. Use [id] [message].\n")
                continue

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: Exe3-DS-ClientP2P-MolinariLorenzo.py <host> <port> <peer_host:peer_port> ...")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    peer_args = sys.argv[3:]

    my_peer = Peer(host, port)

    for peer_arg in peer_args:
        peer_host, peer_port = peer_arg.split(":")
        my_peer.add_peer(peer_host, int(peer_port))

    my_peer.run()
