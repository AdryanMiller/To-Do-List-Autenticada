from bcrypt import hashpw, checkpw, gensalt
from re import fullmatch

def is_valid_email(email):
    padrao = r'^[\w.-]+@[\w.-]+\.\w+$'
    return bool(fullmatch(padrao, email))

def is_empty_string(value):
    if value is None:
        return True
    return not value.strip()

def hash_password(password):
    try:
        password_bytes = password.encode('utf-8')
        password_hash = hashpw(password_bytes, gensalt())
        return password_hash
    except AttributeError as e:
        raise RuntimeError('Erro na hash da senha') from e

def check_password(password, password_hash):
    if password is None or password_hash is None:
        return False
    entered_bytes = password.encode('utf-8')
    return bool(checkpw(entered_bytes, password_hash))



