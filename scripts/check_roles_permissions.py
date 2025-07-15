# 確認用スクリプト例
from app import create_app
from app.database import db
from app.models import Permission

app = create_app()

with app.app_context():
    permissions = Permission.query.filter(Permission.id.in_([4, 11])).all()
    for p in permissions:
        print(p.id, p.name)
