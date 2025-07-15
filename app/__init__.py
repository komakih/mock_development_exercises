from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# DBおよびLoginManagerのインスタンス生成
db = SQLAlchemy()
login_manager = LoginManager()

# 必要なインポートを追加
from app.models import User
from app.modules.auth.routes import auth_bp
from app.modules.profile.routes import profile_bp
from app.modules.admin.routes import admin_bp
from app.modules.chat.routes import chat_bp
from app.modules.faq.routes import faq_bp
from app.modules.history.routes import history_bp
from app.modules.errors.errors import errors_bp
from app.modules.routes.index_update import bp as index_update_bp

def create_app():
    app = Flask(__name__)

    # コンフィグ設定
    app.config.from_pyfile('../instance/config.py', silent=True)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../instance/app.db')

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
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(faq_bp, url_prefix='/faq')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(errors_bp)
    app.register_blueprint(index_update_bp)

    # DBの初回作成
    with app.app_context():
        db.create_all()

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.route('/trigger-error')
    def trigger_error():
        raise Exception('意図的に発生させたテストエラー')

    return app