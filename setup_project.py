import os

# プロジェクトの初期構造を定義
structure = {
    'app': {
        '__init__.py': '',
        'routes.py': '''from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
''',
        'models.py': '''from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('chat_history.id'), nullable=False)
    sender = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
''',
        'templates': {
            'index.html': '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>チャットアプリ</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>チャットアプリへようこそ！</h1>
</body>
</html>'''
        },
        'static': {
            'css': {
                'style.css': '''body {
    font-family: sans-serif;
    padding: 20px;
}'''
            },
            'js': {
                'script.js': '// JavaScriptコードはここに記述します'
            }
        }
    },
    'instance': {},
    'migrations': {},
    'tests': {},
    'requirements.txt': '''Flask>=2.3
Flask-SQLAlchemy
Flask-Migrate
Flask-Login
openai
langchain
llama_index
chromadb''',
    '.gitignore': '''venv/
__pycache__/
instance/*.db
.env
*.pyc''',
    'run.py': '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)'''
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
            print(f'Directory created: {path}')
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'File created: {path}')

if __name__ == '__main__':
    project_name = 'project_root'
    create_structure(project_name, structure)
    print('プロジェクト構造の作成が完了しました。')

