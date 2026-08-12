from src.app.database.connection import connect_db
from src.app.utils.auth_utils import is_empty_string
from src.app.repository.task_repository import create_task_repository,get_task_repository,update_task_repository,delete_task_repository,update_status_repository
from src.app.exceptions import BusinessError

def create_task(user_id:int,title:str,description:str):
    if is_empty_string(title):
        raise BusinessError("Erro: Titulo nao pode estar vazio")

    connection = connect_db()
    try:
        create_task_repository(connection,user_id,title,description)
    finally:
        connection.close()

def list_tasks(user_id:int, filter_task:str):
    if is_empty_string(filter_task) or filter_task not in {'all', 'done', 'pending'}:
        raise BusinessError("Erro: Filter invalido")

    connection = connect_db()
    try:
        tasks = get_task_repository(connection,user_id,filter_task)
        return tasks
    finally:
        connection.close()

def update_task(user_id:int, task_id, title:str, description:str):
    if is_empty_string(title):
        raise BusinessError("Erro: Titulo nao pode estar vazio")
    connection = connect_db()
    try:
        update_task_repository(connection,title,description,task_id,user_id)
    finally:
        connection.close()

def update_task_status(user_id:int, task_id:int, status:str):
    if is_empty_string(status) or status not in {'done', 'pending'}:
        raise BusinessError("Erro: Status invalido")
    connection = connect_db()
    try:
        update_status_repository(connection,task_id,user_id,status)

    finally:
        connection.close()

def delete_task(user_id:int, task_id:int):
    connection = connect_db()
    try:
        delete_task_repository(connection, task_id, user_id)
    finally:
        connection.close()
