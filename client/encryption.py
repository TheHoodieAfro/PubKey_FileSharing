import os, struct
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

FILE_LOCATION = os.path.dirname(__file__)

def generateKeyPair():

    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open(FILE_LOCATION +"/keys/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open(FILE_LOCATION +"/keys/public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def getPrivateKey():

    file_in = open(FILE_LOCATION +'/keys/private.pem','r')
    private_key = RSA.import_key(file_in.read())
    file_in.close()

    return private_key

def getPublicKey():

    file_in = open(FILE_LOCATION +'/keys/public.pem','r')
    public_key = RSA.import_key(file_in.read())
    file_in.close()

    return public_key

def encryptFile(session, file, filename, filesize):

    iv = get_random_bytes(16)
    encryptor = AES.new(session, AES.MODE_CBC, iv)

    chunksize=64*1024
    with open(file, 'rb') as file_in:
        with open(FILE_LOCATION +'/encrypted_data/'+ filename +'.enc', "wb") as file_out:
            file_out.write(struct.pack('<Q', filesize))
            file_out.write(iv)

            while True:
                chunk = file_in.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                file_out.write(encryptor.encrypt(chunk))

def decryptFile(file_name, session_key):

    with open(FILE_LOCATION +'/encrypted_data/'+ file_name, 'rb') as file_in:
        origin_size = struct.unpack('<Q', file_in.read(struct.calcsize('Q')))[0]
        iv = file_in.read(16)
        decryptor = AES.new(session_key, AES.MODE_CBC, iv)
        origin_name = os.path.splitext(file_name)[0]

        chunksize=24*1024
        with open('{}/data/{}'.format(FILE_LOCATION, origin_name), 'wb') as file_out:
            while True:
                chunk = file_in.read(chunksize)
                if len(chunk) == 0:
                    break
                file_out.write(decryptor.decrypt(chunk))

            file_out.truncate(origin_size)

def generateSessionKey():

    return get_random_bytes(16)

def encryptKey(session_key):

    cipher_rsa = PKCS1_OAEP.new(getPublicKey())
    session_key_enc = cipher_rsa.encrypt(session_key)
    return base64.b64encode(session_key_enc)

def decryptKey(session_key_enc):

    cipher_rsa = PKCS1_OAEP.new(getPrivateKey())
    session_key = base64.b64decode(session_key_enc)
    return cipher_rsa.decrypt(session_key)