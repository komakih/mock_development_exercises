from app import create_app
from app.database import db
from app.models import Role, Permission

app = create_app()

roles_permissions = {
    'Admin': [
        'user_list', 'create_user', 'edit_user', 'delete_user',
        'index_ignite',
        'view_chat', 'post_chat', 'edit_chat', 'delete_chat',
        'view_history', 'edit_history', 'delete_history',
        'view_document', 'edit_document', 'delete_document'
    ],
    'Moderator': [
        'user_list', 'create_user', 'edit_user',
        'index_ignite',
        'view_chat', 'post_chat', 'edit_chat', 'delete_chat',
        'view_history', 'edit_history',
        'view_document', 'edit_document'
    ],
    'User': [
        'view_chat', 'post_chat',
        'view_history',
        'view_document'
    ],
    'Guest': [
        'view_chat',
        'view_document'
    ]
}

permissions_desc = {
    'user_list': 'ユーザー一覧',
    'create_user': 'ユーザー作成',
    'edit_user': 'ユーザー情報編集',
    'delete_user': 'ユーザー削除',
    'index_ignite': 'インデックス更新',
    'view_chat': 'チャット閲覧',
    'post_chat': 'チャット投稿',
    'edit_chat': 'チャット編集',
    'delete_chat': 'チャット削除',
    'view_history': '履歴閲覧',
    'edit_history': '履歴編集',
    'delete_history': '履歴削除',
    'view_document': 'ドキュメント閲覧',
    'edit_document': 'ドキュメント編集',
    'delete_document': 'ドキュメント削除'
}

with app.app_context():
    db.create_all()

    # パーミッションを作成
    permissions = {}
    for perm_name, desc in permissions_desc.items():
        permission = Permission.query.filter_by(name=perm_name).first()
        if not permission:
            permission = Permission(name=perm_name, description=desc)
            db.session.add(permission)
        permissions[perm_name] = permission

    # ロールを作成し、パーミッションを割り当て
    for role_name, perms in roles_permissions.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
        role.permissions = [permissions[perm_name] for perm_name in perms]

    db.session.commit()

print("初期ロール・パーミッション設定完了")