import threading
import socket
host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
users = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = users[index]
            broadcast(f'{user} telah meninggalkan room chat !'.encode('utf-8'))
            users.remove(user)
            break
# Main function to receive the clients connection


def receive():
    while True:
        print('Server sedang berjalan dan merekam ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('user?'.encode('utf-8'))
        user = client.recv(1024)
        users.append(user)
        clients.append(client)
        print(f'User dari client ini yaitu : {user}'.encode('utf-8'))
        broadcast(f'{user} Telah bergabung ke dalam chat !'.encode('utf-8'))
        client.send('Kamu telah terhubung !'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
