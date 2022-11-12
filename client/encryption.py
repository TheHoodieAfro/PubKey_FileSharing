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
    f = open(os.path.dirname(__file__) +'/keys/private.pem','r')
    private_key = RSA.import_key(f.read())
    f.close()

    return private_key

def getPublicKey():
    f = open(os.path.dirname(__file__) +'/keys/public.pem','r')
    public_key = RSA.import_key(f.read())
    f.close()

    return public_key

def encryptFile(session, file, filename, filesize):
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

def decryptFile(filename, session_key):

    with open(os.path.dirname(__file__) +'/encrypted_data/'+ filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(session_key, AES.MODE_CBC, iv)
        uno, dos = os.path.splitext(filename)
        chunksize=24*1024

        with open('{}/data/{}'.format(os.path.dirname(__file__), uno), 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

def decryptKey(sessionEnc):

    cipher_rsa = PKCS1_OAEP.new(getPrivateKey())
    return cipher_rsa.decrypt(sessionEnc)

def encryptKey(public_key, session):
    cipherRSA = PKCS1_OAEP.new(public_key)
    return cipherRSA.encrypt(session)

def generateSessionKey():
    return get_random_bytes(16)