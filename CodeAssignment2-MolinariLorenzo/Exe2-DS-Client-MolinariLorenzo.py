import socket
from sys import argv
import message_exe2_pb2  # Import protoc file

def main():
    host = None
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

        while True:
            try:
                sender_id = int(input("Enter sender: "))
                receiver_id = int(input("Enter receiver: "))
                message_content = input("Enter message: ")

                message = message_exe2_pb2.Message()
                message.sender = sender_id
                message.receiver = receiver_id
                message.message = message_content

                serialized_message = message.SerializeToString()
                s.sendall(serialized_message)

                if message_content == "end":
                    break

                data = s.recv(1024)
                response_message = message_exe2_pb2.Message()
                response_message.ParseFromString(data)
                print(f"Reply: {response_message.message}")

            except Exception as e:
                print(f"Error: {e}")
                break

        print("Closing connection")

if __name__ == "__main__":
    main()
