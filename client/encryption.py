import os, struct

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

def generateKeyPair():

    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open(os.path.dirname(__file__) +"/keys/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open(os.path.dirname(__file__) +"/keys/public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def getPrivateKey():

    file_in = open(os.path.dirname(__file__) +'/keys/private.pem','r')
    private_key = RSA.import_key(file_in.read())
    file_in.close()

    return private_key

def getPublicKey():

    file_in = open(os.path.dirname(__file__) +'/keys/public.pem','r')
    public_key = RSA.import_key(file_in.read())
    file_in.close()

    return public_key

def encryptFile(session, file, filename, filesize):

    iv = get_random_bytes(16)
    encryptor = AES.new(session, AES.MODE_CBC, iv)

    chunksize=64*1024
    with open(file, 'rb') as file_in:
        with open(os.path.dirname(__file__) +'/encrypted_data/'+ filename +'.enc', "wb") as file_out:
            file_out.write(struct.pack('<Q', filesize))
            file_out.write(iv)

            while True:
                chunk = file_in.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                file_out.write(encryptor.encrypt(chunk))

def decryptFile(filename, session):

    with open(os.path.dirname(__file__) +'/encrypted_data/'+ filename, 'rb') as file_in:
        origsize = struct.unpack('<Q', file_in.read(struct.calcsize('Q')))[0]
        iv = file_in.read(16)
        decryptor = AES.new(session, AES.MODE_CBC, iv)
        origin_name = os.path.splitext(filename)[0]

        chunksize=24*1024
        with open('{}/data/{}'.format(os.path.dirname(__file__), origin_name), 'wb') as file_out:
            while True:
                chunk = file_in.read(chunksize)
                if len(chunk) == 0:
                    break
                file_out.write(decryptor.decrypt(chunk))

            file_out.truncate(origsize)

def decryptKey(encrypted_session):

    cipher_rsa = PKCS1_OAEP.new(getPrivateKey())
    return cipher_rsa.decrypt(encrypted_session)

def encryptKey(session):

    cipher_rsa = PKCS1_OAEP.new(getPublicKey())
    return cipher_rsa.encrypt(session)

def generateSessionKey():

    return get_random_bytes(16)