import secrets
import string


def generate_bearer_token(token_length=32):
    alphabet = string.ascii_letters + string.digits
    bearer_token = ''.join(secrets.choice(alphabet) for i in range(token_length))
    return bearer_token
