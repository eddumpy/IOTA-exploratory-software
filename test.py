

from Crypto.Cipher import XOR
from iota import TryteString
import base64


def encrypt(plaintext):
    cipher = XOR.new("notaverysecretkey")
    return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(ciphertext):
    cipher = XOR.new("notaverysecretkey")
    return cipher.decrypt(base64.b64decode(ciphertext))


message = 6
mess_str = str(6)
mess_encode = mess_str.encode('utf-8')
print("mess encode = ", mess_encode)
mess_encrypt = encrypt(mess_encode)
print("mess_encrypt = ", mess_encrypt)

l = TryteString.from_bytes(mess_encrypt)

r = l.decode()

print("r = ", r)

w = decrypt(r)
w.decode()
print("w = ", w.decode())


