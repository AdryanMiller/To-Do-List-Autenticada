import pymysql

def create_user(connection, email:str, password_hash:str):
    cursor = None
    try:

        cursor = connection.cursor()
        command_sql = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        cursor.execute(command_sql,(email,password_hash))
        connection.commit()

    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e

    finally:
        if cursor:
            cursor.close()

def find_user_by_email(connection, email:str):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(command_sql,(email,))
        results = cursor.fetchone()
        return results

    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def find_user_by_id(connection, user_id:int):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "SELECT * FROM users WHERE id = %s"
        cursor.execute(command_sql,(user_id,))
        results = cursor.fetchone()
        return results

    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def update_avatar(connection, user_id, avatar):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "UPDATE users SET avatar = %s WHERE id = %s"
        cursor.execute(command_sql, (avatar, user_id))
        connection.commit()
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def update_password(connection, user_id, password_hash:str):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "UPDATE users SET password_hash = %s WHERE id = %s"
        cursor.execute(command_sql, (password_hash, user_id))
        connection.commit()
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def save_totp_secret(connection, user_id, totp_secret):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "UPDATE users SET totp_secret = %s WHERE id = %s"
        cursor.execute(command_sql, (totp_secret, user_id))
        connection.commit()
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def enable_totp(connection, user_id):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "UPDATE users SET totp_enabled = 1 WHERE id = %s"
        cursor.execute(command_sql, (user_id,))
        connection.commit()
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

