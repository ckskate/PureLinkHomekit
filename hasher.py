'''
Transfers the password from the sticker to the needed hash.
'''
import base64
import hashlib


def hash_password(pwd: str) -> str:
  hasher = hashlib.sha512()
  hasher.update(pwd.encode('utf-8'))
  pwd_hash = base64.b64encode(hasher.digest())
  return pwd_hash.decode('utf-8')


if __name__ == "__main__":
  # Ask for the password
  pwd = input("Product WiFi Password (e.g.: adgjsfhk):")

  # Transfer password to hash version
  hash = hashlib.sha512()
  hash.update(pwd.encode('utf-8'))
  pwd_hash = base64.b64encode(hash.digest()).decode('utf-8')

  # Print out password hash
  print(pwd_hash)
