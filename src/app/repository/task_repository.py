import pymysql

def create_task_repository(connection, user_id, title, description):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "INSERT INTO tasks(user_id,title, description) VALUES (%s,%s, %s)"
        cursor.execute(command_sql, (user_id, title, description))
        connection.commit()

    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e

    finally:
        if cursor:
            cursor.close()

def get_task_repository(connection, user_id):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "SELECT title,description,status FROM tasks WHERE user_id = %s"
        cursor.execute(command_sql, (user_id,))
        result = cursor.fetchall()
        return result
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def update_task_repository(connection, title, description, task_id, user_id):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "UPDATE tasks SET title = %s, description = %s WHERE id = %s AND user_id = %s"
        cursor.execute(command_sql, (title, description, task_id, user_id))
        connection.commit()

    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

def delete_task_repository(connection, task_id, user_id):
    cursor = None
    try:
        cursor = connection.cursor()
        command_sql = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
        cursor.execute(command_sql, (task_id, user_id))
        connection.commit()
    except pymysql.Error as e:
        raise RuntimeError('Error inesperado no banco de dados') from e
    finally:
        if cursor:
            cursor.close()

