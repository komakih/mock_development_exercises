from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  # ←追加
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()  # ←追加

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # アプリ設定
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # instanceフォルダ作成
    os.makedirs(app.instance_path, exist_ok=True)

    # DB初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login初期化（重要）← ここを追加！
    login_manager.init_app(app)
    #login_manager.login_view = 'auth.login'  # もしログインページがあれば指定（任意）

    # ユーザーの読み込み関数を指定
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint読み込み
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
