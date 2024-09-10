from datetime import datetime, timedelta, timezone
from functools import wraps
from .models import Admin

import bcrypt
import jwt
from flask import jsonify, session

from app.config import Config

config = Config()
security_key = config.SECRET_KEY
allowed_admins = config.ALLOWED_ADMINS.split(',')


def hash_password(plain_text_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(stored_password_hash: str, provided_password: str) -> bool:
    return bcrypt.checkpw(
        provided_password.encode('utf-8'),
        stored_password_hash.encode('utf-8')
    )


def create_jwt(admin: Admin) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(hours=12)

    payload = {
        'sub': admin.id,
        'name': admin.username,
        'exp': expiration
    }

    token = jwt.encode(payload, security_key, algorithm='HS256')
    return token


def decode_jwt(token: str) -> dict:
    token_bytes = token.encode('utf-8')
    payload = jwt.decode(token_bytes, security_key, algorithms=['HS256'])
    return payload


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'jwt_token' not in session:
            return jsonify({'Error': 'Invalid or missing token'}), 403

        token = session['jwt_token']
        try:
            payload = decode_jwt(token)
        except (IndexError, TypeError):
            return jsonify({'Error': 'Invalid or missing token'}), 403

        username = payload.get('name')
        if not username or username not in allowed_admins:  
            return jsonify({'message': 'Access denied'}), 403

        return func(*args, **kwargs)
    return wrapper
