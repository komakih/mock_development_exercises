import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import Role, Permission

app = create_app()

with app.app_context():
    user_role = Role.query.filter_by(name='User').first()
    post_chat_permission = Permission.query.filter_by(name='post_chat').first()

    if user_role and post_chat_permission:
        user_role.permissions.append(post_chat_permission)
        db.session.commit()
        print("Userロールにpost_chatパーミッションを追加しました。")
    else:
        print("Userロールまたはpost_chatパーミッションが見つかりませんでした。")
