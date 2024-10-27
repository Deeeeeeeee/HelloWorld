import socket
import hello_pb2

def handle_connection(client_socket):
    data = client_socket.recv(1024)
    if data:
        message = hello_pb2.Person()
        message.ParseFromString(data)
        print(f"Received message: Name: {message.name}, Id: {message.id}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8888)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        handle_connection(client_socket)

if __name__ == "__main__":
    start_server()