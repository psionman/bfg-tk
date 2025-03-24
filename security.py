# """Security functions for BfG."""
# import os
# from pathlib import Path
# from cryptography.fernet import Fernet
# from dotenv import load_dotenv

# from constants import USER_DATA_DIR


# def _get_fernet() -> str:
#     load_dotenv(Path(USER_DATA_DIR, '.env'))
#     secret_key = os.getenv('SECRET_KEY')
#     if not secret_key:
#         secret_key = Fernet.generate_key()
#         path = Path(USER_DATA_DIR, '.env')
#         path.parent.mkdir(parents=True, exist_ok=True)
#         with open(path, 'w') as f_env:
#             f_env.write(f'SECRET_KEY={secret_key}')
#     print(secret_key)
#     return Fernet(secret_key)


# def get_password() -> str:
#     with open('pw.txt') as f_pwd:
#         stored_password = f_pwd.read()

#     fernet = _get_fernet()
#     stored_dec_password = fernet.decrypt(stored_password).decode()
#     print(f"Decrypted Password: {stored_dec_password}")


# def save_password(password: str) -> None:
#     fernet = _get_fernet()
#     new_enc_password = fernet.encrypt(password.encode()).decode()

#     with open('pw.txt', 'w') as f_pwd:
#         f_pwd.write(new_enc_password)

#     print(f'Encrypted Password Stored: {new_enc_password}')
