import random
import string


def generate_bearer_token():
    n = 20
    string_val = ''.join(random.choices(string.ascii_letters, k=n))
    return string_val
