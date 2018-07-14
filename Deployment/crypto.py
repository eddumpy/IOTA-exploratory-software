"""
crypto.py

A really basic script for encrypting and decrypting data.

This script is based off of some code found at this link:
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password

Can be edited to provide better encryption algorithms. For this deployment,
"""

from Crypto.Cipher import XOR
import base64


class Crypto:

    def __init__(self):
        self.key = "notaverysecretkey"

    def encrypt(self, data):
        plaintext = str(data).encode('utf-8')
        cipher = XOR.new(self.key)
        return base64.b64encode(cipher.encrypt(plaintext))

    def decrypt(self, ciphertext):
        cipher = XOR.new(self.key)
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        original_data = str(decrypted_data.decode())
        return original_data
