from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from app.database import db
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):  # UserMixinを追加統合する
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')

    prompts = db.relationship('Prompt', backref='user', lazy=True)
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Prompt {self.title}>'

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.String(36), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # ←追加
    title = db.Column(db.String(128))
    user_message = db.Column(db.Text, nullable=False)          # ← 追加
    assistant_message = db.Column(db.Text, nullable=False)     # ← 追加
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # 作成日時を明確化

    messages = db.relationship(
        'ChatMessage',
        backref='history',
        cascade="all, delete-orphan",
        lazy=True
    )  # リレーションシップを明確に定義（カスケード削除）

    def __repr__(self):
        return f'<ChatHistory {self.title}>'

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('chat_history.id'), nullable=False)
    sender = db.Column(db.String(20), nullable=False)  # 'user' or 'bot'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ChatMessage {self.sender}: {self.message[:20]}...>'

class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)