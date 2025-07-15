import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import Role

app = create_app()

with app.app_context():
    user_role = Role.query.filter_by(name='User').first()
    print("Userロールに割り当てられているパーミッション：")
    for permission in user_role.permissions:
        print(permission.name)