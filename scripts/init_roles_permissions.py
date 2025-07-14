from app import create_app
from app.database import db
from app.models import Role, Permission

app = create_app()

with app.app_context():
    admin_role = Role(name='Admin', description='管理者')
    user_role = Role(name='User', description='一般ユーザー')

    db.session.add(admin_role)
    db.session.add(user_role)

    permissions = [
        Permission(name='view_chat', description='チャット閲覧'),
        Permission(name='edit_chat', description='チャット編集'),
        Permission(name='view_history', description='履歴閲覧'),
        Permission(name='edit_history', description='履歴編集')
    ]
    db.session.add_all(permissions)
    db.session.commit()

    admin_role.permissions.extend(permissions)

    user_permissions = [p for p in permissions if p.name in ('view_chat', 'view_history')]
    user_role.permissions.extend(user_permissions)

    db.session.commit()
    print("初期データの設定が完了しました。")