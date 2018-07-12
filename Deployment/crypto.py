"""
crypto.py

A really basic script for encrypting and decrypting data.

This script is based off of some code found at this link:
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
"""

from Crypto.Cipher import XOR
import base64


class Crypto:

    def __init__(self):
        self.key = "notaverysecretkey"

    def encrypt(self, plaintext):
        cipher = XOR.new(self.key)
        return base64.b64encode(cipher.encrypt(plaintext))

    def decrypt(self, ciphertext):
        cipher = XOR.new(self.key)
        return cipher.decrypt(base64.b64decode(ciphertext))