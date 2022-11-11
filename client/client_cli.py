import os
import socket
import struct
import sys

import tqdm
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

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

session = get_random_bytes(16)
f = open(os.path.dirname(__file__) +'/public_keys/public.pem','r')
public_key = RSA.import_key(f.read())
f.close()

cipherRSA = PKCS1_OAEP.new(public_key)
sessionEnc = cipherRSA.encrypt(session)

iv = get_random_bytes(16)
encryptor = AES.new(session, AES.MODE_CBC, iv)

chunksize=64*1024
with open(file, 'rb') as infile:
        with open(os.path.dirname(__file__) +'/encrypted_data/'+ filename +'.enc', "wb") as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

filename = filename +'.enc'
file = os.path.dirname(__file__) +'/encrypted_data/'+ filename
filesize = os.path.getsize(file)

s.send(sessionEnc)
sent = filename +""+ SEPARATOR +""+ str(filesize)
print(sent)
print(sent.encode())
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