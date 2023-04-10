from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)


key = Fernet.generate_key()
a = 'mateo gowno'
token = encrypt(a.encode(), key)
print(token)
a = decrypt(token, key).decode()
print(a)
#     f.write(token)
# with open('CREDS/creds.txt', 'wb') as f:
