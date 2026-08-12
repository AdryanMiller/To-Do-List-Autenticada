from src.app.database.connection import connect_db
from src.app.repository.user_repository import update_avatar, update_password, find_user_by_id
from src.app.utils.auth_utils import is_empty_string, hash_password, check_password,is_valid_password
from src.app.exceptions import BusinessError

VALID_AVATARS = {'avatar_01', 'avatar_02'}

def update_avatar_service(user_id, avatar):
    if avatar not in VALID_AVATARS:
        raise BusinessError('Avatar não é valido')
    connection = connect_db()
    try:
        update_avatar(connection, user_id, avatar)
    finally:
        connection.close()

def update_password_service(user_id, current_password, new_password):
    erro = is_valid_password(new_password)
    if erro:
        raise BusinessError(erro)
    connection = connect_db()
    try:
        user = find_user_by_id(connection, user_id)
        if not user :
            raise BusinessError('Erro: 400, Usuario não existente')
        if not check_password(current_password, user['password_hash']):
            raise BusinessError('Erro: Campo incorreto')
        hashed_password = hash_password(new_password)
        update_password(connection, user_id, hashed_password)
    finally:
        connection.close()

