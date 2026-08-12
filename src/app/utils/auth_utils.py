from bcrypt import hashpw, checkpw, gensalt
from re import fullmatch, search


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
    if isinstance(password_hash, str):
        password_hash = password_hash.encode('utf-8')
    entered_bytes = password.encode('utf-8')
    return bool(checkpw(entered_bytes, password_hash))

def is_valid_password(password):
    if password is None:
        return "Senha não pode ser vazia"
    if len(password) < 8 or len(password) > 14:
        return "Senha deve conter de 8 a 14 caracteres"
    if not search(r"[A-Z]", password):
        return "Senha deve conter pelo menos 1 caractere maiúsculo"
    if not search(r"\d", password):
        return "Senha deve conter pelo menos 1 número"
    return None

