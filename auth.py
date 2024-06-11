# to add authorization in the future
# taken from a cs310 project starter code



#
# auth.py
#
# Handles common authentication tasks.
#
# Original author:
#   Dilan Nair
#   Northwestern University
#

import bcrypt


def hash_password(password, salt_rounds=12):
  """
  Hashes a password.

  Parameters
  ----------
  password : str
    The password to hash.
  salt_rounds : int
    The number of rounds of hashing to apply. Defaults to 12.
  
  Returns
  -------
  str
    The hashed password.
  """

  if len(password) > 72:
    raise ValueError("Password must be less than 72 characters.")

  salt = bcrypt.gensalt(salt_rounds)
  hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

  return hashed.decode('utf-8')


def check_password(password, hashed):
  """
  Checks a password against a hash.

  Parameters
  ----------
  password : str
    The password to check.
  hashed : str
    The hash to check against.

  Returns
  -------
  bool
    True if the password is correct, False otherwise.
  """

  return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

