"""transfers the password from the sticker to the needed hash."""

import base64
import hashlib


def hash_password(pwd: str) -> str:
  """takes a given password and return the sha512 hash."""

  hasher = hashlib.sha512()
  hasher.update(pwd.encode('utf-8'))
  pwd_hash = base64.b64encode(hasher.digest())
  return pwd_hash.decode('utf-8')
