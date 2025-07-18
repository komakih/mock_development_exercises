from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary='user_roles', backref='users')

    def set_password(self, password):
        from werkzeug.security import generate_password_hash  # メソッド内にimportを追加（重要）
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash  # メソッド内にimportを追加（重要）
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission_name):
        return any(permission.name == permission_name for role in self.roles for permission in role.permissions)
    
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

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    permissions = db.relationship('Permission', secondary='role_permissions', backref='roles')

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    role_permissions = db.Table('role_permissions',
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
        db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'), primary_key=True)
    )

    user_roles = db.Table('user_roles',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
    )

class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(255), unique=True, nullable=False)
    config_value = db.Column(db.Text, nullable=False)

    @staticmethod
    def get_config(key):
        config = AppConfig.query.filter_by(config_key=key).first()
        return config.config_value if config else None

    @staticmethod
    def set_config(key, value):
        config = AppConfig.query.filter_by(config_key=key).first()
        if config:
            config.config_value = value
        else:
            config = AppConfig(config_key=key, config_value=value)
            db.session.add(config)
        db.session.commit()