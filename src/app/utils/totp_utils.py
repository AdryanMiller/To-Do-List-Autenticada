import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def generate_totp_uri(secret, email):
    if secret is None or email is None:
        raise TypeError('Erro: Secret ou Email invalido')
    try:
        totp = pyotp.TOTP(secret).provisioning_uri(
            name=email,
            issuer_name = 'Todolist'
        )
        return totp
    except AttributeError as e:
        raise RuntimeError('Erro: gerar totp url') from e

def verify_totp_code(secret, code):
    if secret is None or code is None:
        raise TypeError('Erro: Secret ou Code invalido')
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    except AttributeError as e:
        raise RuntimeError('Erro: Veriicacao de codigo') from e
