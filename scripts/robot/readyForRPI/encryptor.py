from Crypto.Cipher import AES

class Encryptor:
        key = b'2r5u7x!A%D*G-KaP'
        iv = b'This is an IV456'
        print(key, iv)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        print('thats alot of cipher')

        # Encrypts message
        def encrypt(self, _string):
                return self.cipher.encrypt(_string)

        # Decrypts message
        def decrypt(self, ciphertext):
                return self.cipher.decrypt(ciphertext)
