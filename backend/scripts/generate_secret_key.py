from cryptography.fernet import Fernet

# Fernetキーの生成
key = Fernet.generate_key()

print(key)
