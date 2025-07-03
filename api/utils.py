import bcrypt
import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# パスワードのハッシュ化
def hash_password(plain_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# パスワード検証
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWTトークン作成
def create_jwt_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token

# JWTトークン検証（後でAPI保護に使用）
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

import logging
from logging.handlers import RotatingFileHandler
import os

# ログファイルのディレクトリを作成（存在しなければ）
log_directory = "./logs"
os.makedirs(log_directory, exist_ok=True)

# エラーログの設定
def setup_error_logger():
    logger = logging.getLogger("error_logger")
    logger.setLevel(logging.ERROR)
    handler = RotatingFileHandler(f"{log_directory}/error.log", maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# アクセスログの設定
def setup_access_logger():
    logger = logging.getLogger("access_logger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(f"{log_directory}/access.log", maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
