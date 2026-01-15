from hashlib import sha256
from secrets import token_urlsafe
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_hash.hash(password)

def generate_session_id():
    return token_urlsafe(32)

def hash_session_id(session_id: str):
    return sha256(session_id.encode()).hexdigest()

def verify_session(session_id: str, session_id_hash: str):
    return hash_session_id(session_id) == session_id_hash