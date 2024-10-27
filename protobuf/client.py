import socket
import hello_pb2

def send_protobuf_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)

    try:
        client_socket.connect(server_address)

        # 创建要发送的Protobuf消息对象
        message = hello_pb2.Person()
        message.name = "John Doe"
        message.id = 30

        # 将Protobuf消息对象序列化为二进制数据
        serialized_data = message.SerializeToString()

        client_socket.send(serialized_data)
        print("Protobuf message sent successfully.")

    except ConnectionError as e:
        print(f"Error connecting to server: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    send_protobuf_request()