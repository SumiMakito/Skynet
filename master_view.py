import base64
import os

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def decrypt_valuables(f):
    try:
        # probably the file is not encrypted
        print(str(f, 'ascii'))
        print('Content is not encrypted!')
        return
    except UnicodeDecodeError:
        # byte binary
        pass
    # open and read the private key
    private_key = open(os.path.join('master_keys', 'master_rsa')).read()
    # import the private rsa key
    private_rsa_key = RSA.importKey(private_key)
    # cipher used to decrypt the file
    cipher = PKCS1_v1_5.new(private_rsa_key)
    # get to know the size of SHA-1 digest
    digest_size = SHA.digest_size
    # create a random sentinel according to the digest size
    sentinel = Random.new().read(15 + digest_size)
    # decrypt
    decrypted_data = cipher.decrypt(f, sentinel)
    # get the digest of the content
    digest = SHA.new(decrypted_data[digest_size:]).digest()
    # print the text if the two digest values match
    if digest == decrypted_data[:digest_size]:
        print(str(decrypted_data[digest_size:], 'ascii'))
    else:
        print('Digest does not match!')


if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    decrypt_valuables(f)
