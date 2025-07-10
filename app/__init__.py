from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# DBおよびLoginManagerのインスタンス生成
db = SQLAlchemy()
login_manager = LoginManager()

# 必要なインポートを追加
from app.models import User
from app.modules.auth.routes import auth_bp
from app.modules.profile.routes import profile_bp
from app.modules.admin.routes import admin_bp

def create_app():
    app = Flask(__name__)

    # コンフィグ設定
    app.config.from_pyfile('../instance/config.py', silent=True)

    # DB初期化
    db.init_app(app)

    # Flask-Login設定
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint登録
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # DBの初回作成
    with app.app_context():
        db.create_all()

    return app