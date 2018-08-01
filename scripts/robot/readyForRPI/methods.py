from Crypto.Cipher import AES
from base64 import b64encode, b64decode

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)).encode()
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
key = b'2r5u7x!A%D*G-KaP'
iv = b'This is an IV456'

def encrypt(message):
    raw = pad(message.encode())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return b64encode(cipher.encrypt(raw))

def decrypt(message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(b64decode(message))).decode()
