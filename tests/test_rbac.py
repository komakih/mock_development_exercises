import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import User, Role, Permission
from app.modules.auth.auth import require_permission
from flask_login import login_user

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.app_context():
        db.create_all()

        admin_role = Role(name='Admin', description='管理者')
        user_role = Role(name='User', description='一般ユーザー')

        perms = [
            Permission(name='view_chat', description='チャット閲覧'),
            Permission(name='edit_chat', description='チャット編集'),
            Permission(name='view_history', description='履歴閲覧'),
            Permission(name='edit_history', description='履歴編集')
        ]

        db.session.add_all([admin_role, user_role] + perms)
        db.session.commit()

        admin_role.permissions.extend(perms)
        user_role.permissions.extend(perms[:2])

        db.session.commit()

        # ここにルートを追加（重要！）
        @app.route('/some_protected_route')
        @require_permission('edit_history')
        def protected_route():
            return "許可されました", 200

        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_roles_permissions_created(app):
    assert Role.query.filter_by(name='Admin').first() is not None
    assert Permission.query.filter_by(name='view_chat').first() is not None

def test_default_role_on_user_registration(app):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    default_role = Role.query.filter_by(name='User').first()
    user.roles.append(default_role)
    db.session.add(user)
    db.session.commit()
    assert 'User' in [role.name for role in user.roles]

def test_role_permissions(app):
    role = Role.query.filter_by(name='User').first()
    permissions = [perm.name for perm in role.permissions]
    assert 'view_chat' in permissions
    assert 'edit_chat' in permissions

def test_route_permission(client, app):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password')
    default_role = Role.query.filter_by(name='User').first()
    user.roles.append(default_role)
    db.session.add(user)
    db.session.commit()

    with client:
        # ユーザーをログイン状態に設定
        with app.test_request_context():
            login_user(user)

        response = client.get('/some_protected_route')
        assert response.status_code == 403
