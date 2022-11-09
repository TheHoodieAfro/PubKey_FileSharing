import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP


def generateKeyPair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("./keys/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("./keys/public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

def getPrivateKey():
    f = open('./keys/private.pem"','r')
    private_key = RSA.import_key(f.read())
    f.close()

    return private_key

def getPublicKey():
    f = open('./keys/public.pem"','r')
    public_key = RSA.import_key(f.read())
    f.close()

    return public_key


def decryptFile(file):

    count_files = 0
    dir_path = './data'
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count_files += 1

    if count_files >= 100:
        for path in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, path))

    private_key = getPrivateKey()
    crypted_session, nonce, tag, ciphertext = [ file.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session = cipher_rsa.decrypt(crypted_session)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    c = 0
    while True:
        path = "./data/file{}.txt".format(c)
        if os.path.exists(path):
            decryptedFile = open(path, "w")
            break
        c += 1

    decryptedFile.write(data.decode("utf-8"))
    decryptedFile.close()

    return decryptedFile
