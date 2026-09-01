from src.app.database.connection import connect_db
from src.app.repository.user_repository import find_user_by_email, create_user, find_user_by_id, save_totp_secret, enable_totp
from src.app.utils.auth_utils import is_valid_email, is_empty_string, hash_password, check_password, is_valid_password
from src.app.utils.totp_utils import generate_totp_secret, generate_totp_uri, verify_totp_code
from src.app.exceptions import BusinessError

def register_user(email:str,password:str):
    if is_empty_string(email) or is_empty_string(password):
        raise BusinessError('Email e senha são obrigatorios')
    if not is_valid_email(email):
        raise BusinessError('Email invalido')
    erro = is_valid_password(password)
    if erro:
        raise BusinessError(erro)
    connection = connect_db()
    try:
        if find_user_by_email(connection, email):
            raise BusinessError('Erro: 400, email existente')
        password_hash = hash_password(password)
        create_user(connection, email, password_hash)
    finally:
        connection.close()

def login_user(email:str,password:str):
    if is_empty_string(email) or is_empty_string(password):
        raise BusinessError('Email e senha sao obrigatorios')
    if not is_valid_email(email):
        raise BusinessError('Email invalido')
    connection = connect_db()
    try:
        user = find_user_by_email(connection, email)
        if not user:
            raise BusinessError('Erro: 400, Email ou senha invalido')

        if not check_password(password, user['password_hash']):
            raise BusinessError('Erro: 400, Email ou senha invalido')

        return user
    finally:
        connection.close()

def start_totp_setup(user_id:int):
    connection = connect_db()
    try:
        user = find_user_by_id(connection, user_id)
        if not user :
            raise BusinessError('Erro: 400, Usuario não existente')
        generate_secret_totp = generate_totp_secret()
        save_totp_secret(connection, user_id, generate_secret_totp)
        return generate_totp_uri(generate_secret_totp, user['email'])
    finally:
        connection.close()

def confirm_totp_setup(user_id:int, code):
    connection = connect_db()
    try:
        user = find_user_by_id(connection, user_id)
        if not user:
            raise BusinessError('Erro: 400, Usuario não existente')
        code_valid = verify_totp_code(user['totp_secret'], code)
        if not code_valid:
            raise BusinessError('Erro: 400, Codigo invalido')
        enable_totp(connection, user_id)
    finally:
        connection.close()

def verify_totp_login(user_id:int, code):
    connection = connect_db()
    try:
        user = find_user_by_id(connection, user_id)
        if not user:
            raise BusinessError('Erro: 400, Usuario não existente')
        code_valid = verify_totp_code(user['totp_secret'], code)
        if not code_valid:
            raise BusinessError('Erro: 400, Codigo invalido')
    finally:
        connection.close()

