from flask import Flask
from app.database import db
from flask_login import LoginManager

# 各モジュールのBlueprintをインポート
from app.modules.auth.routes import auth_bp
from app.modules.profile.routes import profile_bp
from app.modules.admin.routes import admin_bp

def create_app():
    app = Flask(__name__)

    # コンフィグの設定
    app.config.from_pyfile('../instance/config.py', silent=True)

    # DB初期化
    db.init_app(app)

    # Flask-Login設定
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Blueprintをアプリに登録
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # DBの初回作成
    with app.app_context():
        db.create_all()

    return app
