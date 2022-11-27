import socket
import tqdm
import os
import time

from encryption import generateKeyPair, decryptFile, decryptKey, hashFile

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

SERVER_HOST = "localhost"
SERVER_PORT = 5001

FILE_LOCATION = os.path.dirname(__file__)

server_socket = socket.socket()
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = server_socket.accept() 
print(f"[+] {address} is connected.")

keys_path = FILE_LOCATION +'/keys/'
if not os.path.exists(keys_path +'private.pem') or not os.path.exists(keys_path +'public.pem'):
    generateKeyPair()

public_key_file = FILE_LOCATION +'/keys/public.pem'
public_key_name = os.path.basename(public_key_file)
public_key_size = os.path.getsize(public_key_file)

sent = public_key_name +""+ SEPARATOR +""+ str(public_key_size)
client_socket.send(sent.encode())

progress_bar = tqdm.tqdm(range(public_key_size), f"Sending {public_key_name}", unit="B", unit_scale=True, unit_divisor=1024)
with open(public_key_file, "rb") as file_out:
    while True:

        bytes_readed = file_out.read(BUFFER_SIZE)
        if not bytes_readed:
            break

        client_socket.sendall(bytes_readed)

        progress_bar.update(len(bytes_readed))

session_key_enc = client_socket.recv(BUFFER_SIZE)
session_key = decryptKey(session_key_enc)

file_enc_package_encoded = client_socket.recv(BUFFER_SIZE)

file_enc_package = file_enc_package_encoded.decode()
file_enc_name, file_enc_size = file_enc_package.split(SEPARATOR)
file_enc_name = os.path.basename(file_enc_name)
file_enc_size = int(file_enc_size)

progress_bar = tqdm.tqdm(range(file_enc_size), f"Receiving {file_enc_name}", unit="B", unit_scale=True, unit_divisor=1024)
with open('{}/encrypted_data/{}'.format(FILE_LOCATION, file_enc_name), "wb") as file_in:
    total_recieved = 0
    while True:
        if total_recieved >= file_enc_size:
            break
        bytes_readed = client_socket.recv(BUFFER_SIZE)
        total_recieved = len(bytes_readed)
        if not bytes_readed:
            break

        file_in.write(bytes_readed)
        total_recieved += len(bytes_readed)

        progress_bar.update(len(bytes_readed))

decryptFile(file_enc_name, session_key)

hash_rcv = client_socket.recv(BUFFER_SIZE).decode()

print('Calculated hash'+ hashFile('{}/data/{}'.format(FILE_LOCATION, os.path.splitext(file_enc_name)[0])))
print('Recieved hash'+ hash_rcv)

if hashFile('{}/data/{}'.format(FILE_LOCATION, os.path.splitext(file_enc_name)[0])) == hash_rcv:
    print('POGGERS')
else:
    print('PEPESAD')

client_socket.close()
server_socket.close()