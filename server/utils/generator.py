import hashlib
import random
import string


def generate_bearer_token():
    n = 20
    string_val = ''.join(random.choices(string.ascii_letters, k=n))
    return string_val


def generate_cfa_token():
    token = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()

    return token
