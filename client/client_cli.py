import os
import socket
import sys
import tqdm
import time

from encryption import encryptFile, encryptKey, generateSessionKey

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

SERVER_HOST = "localhost"
SERVER_PORT = 5001

file = sys.argv[1]
filename = os.path.basename(file)
filesize = os.path.getsize(file)

client_socket = socket.socket()

print(f"[+] Connecting to {SERVER_HOST}:{SERVER_PORT}")
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

public_key_package = client_socket.recv(BUFFER_SIZE).decode()
public_key_name, public_key_size = public_key_package.split(SEPARATOR)

public_key_name = os.path.basename(public_key_name)
public_key_size = int(public_key_size)

progress_bar = tqdm.tqdm(range(public_key_size), f"Receiving {public_key_name}", unit="B", unit_scale=True, unit_divisor=1024)
with open('{}/keys/{}'.format(os.path.dirname(__file__), public_key_name), "wb") as file_in:
    total_recieved = 0
    while True:
        if total_recieved >= public_key_size:
            break
        bytes_readed = client_socket.recv(BUFFER_SIZE)
        total_recieved = len(bytes_readed)
        if not bytes_readed:
            break

        file_in.write(bytes_readed)
        total_recieved += len(bytes_readed)

        progress_bar.update(len(bytes_readed))

session_key = generateSessionKey()

session_key_enc = encryptKey(session_key)

encryptFile(session_key, file, filename, filesize)

filename_enc = filename +'.enc'
file_enc = os.path.dirname(__file__) +'/encrypted_data/'+ filename_enc
filesize_enc = os.path.getsize(file_enc)

client_socket.send(session_key_enc)

sent = filename_enc +""+ SEPARATOR +""+ str(filesize_enc)
test = sent.encode()
client_socket.send(test)

time.sleep(0.5)

progress_bar = tqdm.tqdm(range(filesize_enc), f"Sending {filename_enc}", unit="B", unit_scale=True, unit_divisor=1024)
with open(file_enc, "rb") as file_out:
    while True:

        bytes_readed = file_out.read(BUFFER_SIZE)
        if not bytes_readed:
            break

        client_socket.sendall(bytes_readed)

        progress_bar.update(len(bytes_readed))

client_socket.close()