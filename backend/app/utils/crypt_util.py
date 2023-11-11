from cryptography.fernet import Fernet
from decouple import config


secret_key = config("SECRET_KEY")
cipher_suite = Fernet(secret_key)


def encrypt(data: str):
    '''
    Encrypt data.
    '''
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt(data: bytes):
    '''
    Decrypt data.
    '''
    return cipher_suite.decrypt(data).decode()
