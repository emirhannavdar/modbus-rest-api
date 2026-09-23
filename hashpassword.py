from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

password = "deneme123"

hashed = password_hash.hash(password)

print(hashed)
