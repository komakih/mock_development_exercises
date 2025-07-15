import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import User, Role

app = create_app()

with app.app_context():
    user = User.query.filter_by(username='admintest').first()
    admin_role = Role.query.filter_by(name='Admin').first()

    if user and admin_role:
        user.roles.append(admin_role)
        db.session.commit()
        print(f"ロール「Admin」をユーザー「{user.username}」に割り当てました。")
    else:
        print("ユーザーまたはAdminロールが見つかりませんでした。")
