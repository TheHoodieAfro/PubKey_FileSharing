import socket
import tqdm
import os

from encryption import generateKeyPair, getPrivateKey, getPublicKey

SERVER_HOST = "localhost"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

generateKeyPair()
privateKey = getPrivateKey()

file = os.path.dirname(__file__) +'/keys/public.pem'
filename = os.path.basename(file)
filesize = os.path.getsize(file)

client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(file, "rb") as f:
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        client_socket.sendall(bytes_read)

        progress.update(len(bytes_read))

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open('{}/data/{}'.format(os.path.dirname(__file__), filename), "wb") as f:
    total = 0
    while True:
        if total >= filesize:
            break
        bytes_read = client_socket.recv(BUFFER_SIZE)
        total = len(bytes_read)
        if not bytes_read:
            break

        f.write(bytes_read)
        total += len(bytes_read)

        progress.update(len(bytes_read))

client_socket.close()
s.close()