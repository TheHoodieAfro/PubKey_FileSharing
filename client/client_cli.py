import os
import socket
import sys

import tqdm
from encryption import encryptFile, encryptKey, getPublicKey, generateSessionKey

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

host = "localhost"
port = 5001

file = sys.argv[1]
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
with open('{}/keys/{}'.format(os.path.dirname(__file__), filenameTest), "wb") as f:
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

session = generateSessionKey()

sessionEnc = encryptKey(session)

encryptFile(session, file, filename, filesize)

filename = filename +'.enc'
file = os.path.dirname(__file__) +'/encrypted_data/'+ filename
filesize = os.path.getsize(file)

s.send(sessionEnc)
sent = filename +""+ SEPARATOR +""+ str(filesize)
s.send(sent.encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(file, "rb") as f:
    while True:

        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break

        s.sendall(bytes_read)

        progress.update(len(bytes_read))

s.close()