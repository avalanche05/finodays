import hashlib
import random
import string

from data.user import User
from data.token import Token


def generate_bearer_token(user: User):
    n = 20
    string_val = ''.join(random.choices(string.ascii_letters, k=n))
    token = Token()
    token.value = string_val
    token.user_id = user.id
    token.is_alive = True
    return token


def generate_cfa_token():
    token = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()

    return token