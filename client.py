import socket
import threading

HOST = input("Enter server IP: ")  # Example: 127.0.0.1 or 192.168.x.x
PORT = 12345

nickname = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except:
            print("An error occurred. Disconnecting...")
            client.close()
            break

def write():
    while True:
        msg = f'{nickname}: {input("")}'
        client.send(msg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
