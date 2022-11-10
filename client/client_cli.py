import socket
import tqdm
import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = "localhost"
port = 5001

file = input('file to send: ')
filename = os.path.basename(file)
filesize = os.path.getsize(file)

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

received = s.recv(BUFFER_SIZE).decode()
filenameTest, filesizeTest = received.split(SEPARATOR)
filenameTest = os.path.basename(filenameTest)
filesizeTest = int(filesizeTest)

progress = tqdm.tqdm(range(filesizeTest), f"Receiving {filenameTest}", unit="B", unit_scale=True, unit_divisor=1024)
with open('{}/public_keys/{}'.format(os.path.dirname(__file__), filenameTest), "wb") as f:
    total = 0
    while True:
        if total >= filesizeTest:
            break
        bytes_read = s.recv(BUFFER_SIZE)
        total = len(bytes_read)
        if not bytes_read:
            break

        f.write(bytes_read)
        total += len(bytes_read)

        progress.update(len(bytes_read))

session_key = get_random_bytes(16)

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(file, "rb") as f:
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        s.sendall(bytes_read)

        progress.update(len(bytes_read))

s.close()