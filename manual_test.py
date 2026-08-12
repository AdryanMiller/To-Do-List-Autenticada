from src.app.service.user_service import update_avatar_service,update_password_service
from src.app.service.task_service import create_task,list_tasks,update_task,delete_task,update_task_status
from src.app.service.auth_service import register_user,login_user,start_totp_setup,confirm_totp_setup,verify_totp_login
from src.app.exceptions import BusinessError

# try:
#     user = register_user('teste@teste.com','Senha123')
#     print(user)
# except BusinessError as e:
#     print(e)


import pyotp

user = login_user('teste@teste.com','Senha123456')
print(user)
secret = "KS3ETB6JO6DRKOE62QCXKXZPMQNUM27Y"
totp = pyotp.TOTP(secret)
corret_code = totp.now()
print(corret_code)
verify_totp_login(1,0000000)


