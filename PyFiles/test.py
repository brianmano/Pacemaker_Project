from cryptography.fernet import Fernet
from program_files.mode_variables import *

password = "nope"

encryptedpass = encrypt_password(password)

print(encryptedpass)

decryptedpass = decrypt_password(encryptedpass)

print(decryptedpass)
