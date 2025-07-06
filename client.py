import socket
import threading
from datetime import datetime


HOST = '127.0.0.1'  # Accept connections from 127.0.0.1 only
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] {msg.decode('utf-8')}")

            broadcast(msg, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the chat.'.encode('utf-8'), client)
            names.remove(name)
            break

def receive():
    print("Server is running and waiting for connections...")
    while True:
        client, addr = server.accept()
        print(f"Connected with {str(addr)}")

        client.send("NICKNAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f"Name of the client is {name}")
        broadcast(f"{name} joined the chat!".encode('utf-8'), client)
        client.send("Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()
# if you want the server to not send the message so just replace the below code with recieve()
# Let server send messages too
while True:
    msg = input()
    if msg.lower() == 'exit':
        break
    now = datetime.now().strftime("%H:%M:%S")
    full_msg = f"[{now}] Server: {msg}"
    print(full_msg)
    broadcast(full_msg.encode('utf-8'), sender=None)
