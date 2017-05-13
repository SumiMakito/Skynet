import os

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS


def sign_file(f):
    # open private key of master, and then read it
    private_key = open(os.path.join('master_keys', 'master_rsa')).read()
    # import the private rsa key
    private_rsa_key = RSA.importKey(private_key)
    # get the digest of the content
    digest = SHA.new()
    digest.update(f)
    # sign the digest with private key
    signer = PKCS1_PSS.new(private_rsa_key)
    signature = signer.sign(digest)
    # insert the encoded signature before the comma that splits the signature and the content
    return signature + f


if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)
