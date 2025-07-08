import os, openai
from dotenv import load_dotenv
from flask import render_template, redirect, url_for, flash, Flask, request, jsonify
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import db, User, ChatHistory
import uuid
import sys
sys.path.append('/Users/hkomaki/Downloads/mock_development_exercises')

from models import ChatHistory

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))

app.secret_key = '6c2ca336c9b12674bc6df1ab4403c806'
openai.api_key = os.getenv("OPENAI_API_KEY")

# DB設定（SQLiteの例）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hkomaki/Downloads/mock_development_exercises/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)

# Flask-Loginの設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB初期化
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Hello, Flask is working!"

# ログインルート
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('ログインに成功しました。', 'success')
            return redirect(url_for('user_index'))
        else:
            flash('メールアドレスまたはパスワードが間違っています。', 'danger')
    return render_template('login.html', form=form)

# ユーザー登録ルート
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('このメールアドレスは既に登録されています。', 'warning')
            return redirect(url_for('register'))
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('ユーザー登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# ログアウトルート
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('login'))

# ユーザーインデックスルート
@app.route('/index')
@login_required
def user_index():
    return f"こんにちは、{current_user.username}さん！ログインに成功しました。"

# チャットルート
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    response = None
    question = None
    if request.method == 'POST':
        question = request.form.get('question')

        # OpenAI APIに質問を送信して回答を取得する処理
        api_response = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": question}
            ]
        )

        response = api_response.choices[0].message.content

    return render_template('chat.html', response=response, question=question)

# チャットAPIルート（JSON形式でのやり取り用）
@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    user_input = request.json.get('message')
    thread_id = request.json.get('thread_id') or str(uuid.uuid4())

    # OpenAI APIを使用した回答取得処理
    api_response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": user_input}
        ]
    )

    assistant_response = api_response.choices[0].message.content

    # 履歴タイトル生成（最初の質問を利用）
    title = user_input if len(user_input) <= 20 else user_input[:20] + '...'

    # ChatHistoryに履歴を追加・保存
    history_entry = ChatHistory(
        thread_id=thread_id,
        title=title,
        user_message=user_input,
        assistant_message=assistant_response
    )
    db.session.add(history_entry)
    db.session.commit()

    return jsonify({
        'thread_id': thread_id,
        'assistant_message': assistant_response
    })

# 履歴一覧表示
@app.route('/history')
@login_required
def history():
    threads = db.session.query(
        ChatHistory.thread_id,
        ChatHistory.title,
        db.func.max(ChatHistory.timestamp)
    ).group_by(ChatHistory.thread_id).all()
    return render_template('history.html', threads=threads)

# 履歴の個別スレッド表示
@app.route('/history/<thread_id>')
@login_required
def history_thread(thread_id):
    messages = ChatHistory.query.filter_by(thread_id=thread_id).order_by(ChatHistory.timestamp).all()
    return render_template('chat.html', messages=messages, thread_id=thread_id)

if __name__ == '__main__':
    app.run(debug=True)
