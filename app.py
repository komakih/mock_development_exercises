import os, openai, chromadb, uuid
from openai import OpenAI as OpenAIClient 
from dotenv import load_dotenv
from flask import render_template, redirect, url_for, flash, Flask, request, jsonify
from flask_migrate import Migrate
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from models import db, User, ChatHistory, ChatMessage
from openai_utils import generate_thread_title
from llama_index.core import VectorStoreIndex, StorageContext, Settings, PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL
from chromadb.config import Settings as ChromaSettings

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))

app.secret_key = '6c2ca336c9b12674bc6df1ab4403c806'
openai_api_key = os.getenv("OPENAI_API_KEY").strip()

# OpenAIライブラリ側の設定
openai.api_key = openai_api_key
openai.base_url = "https://api.openai.com/v1"  # base_urlを明示的に指定

# LlamaIndex側での明示的APIキー設定
Settings.llm = OpenAI(api_key=openai_api_key)

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-ada-002",
    api_key=openai_api_key,
    timeout=60,
    max_retries=2
    # base_urlなど他の引数は一切指定しない（OpenAI側の設定を使用）
)

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

# ChromaDBとLlamaIndexの設定
INDEX_DIR = "./index_storage"
chroma_client = chromadb.PersistentClient(
    path=INDEX_DIR, 
    settings=ChromaSettings(anonymized_telemetry=False)
)

chroma_collection = chroma_client.get_or_create_collection("document_collection")

# ChromaDBとの連携を設定
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 日本語用QAプロンプト設定（最新版対応）
japanese_prompt = PromptTemplate(DEFAULT_TEXT_QA_PROMPT_TMPL).partial_format(
    context_str="以下の文脈情報を参照して、質問に日本語で答えてください。"
)

rag_index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context=storage_context
)

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

# RAGチャットルート
@app.route('/rag_chat')
@login_required
def rag_chat():
    return render_template('rag_chat.html')

# チャットAPIルート（RAGを用いた社内文書検索機能）
@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    user_input = request.json.get('message')
    thread_id = request.json.get('thread_id') or str(uuid.uuid4())

    # LlamaIndexを使用して社内文書から回答を生成
    query_engine = rag_index.as_query_engine(text_qa_template=japanese_prompt)
    response = query_engine.query(user_input)
    assistant_response = response.response.strip()

    # ソース情報を抽出（回答に関連する文書ノード）
    sources = "\n".join([f"[類似度: {node.score:.2f}] {node.text}" for node in response.source_nodes])

    no_info_messages = [
        "関連する情報が見つかりませんでした",
        "提供された文脈情報からは",
        "申し訳ありませんが"
    ]

    # 関連文書が空、または回答に特定のフレーズが含まれる場合、外部GPT-4を利用
    if (not response.source_nodes) or any(msg in assistant_response for msg in no_info_messages):
        # OpenAIクライアントを明示的に初期化
        openai_client = OpenAIClient(api_key=openai_api_key)  # 明確に修正済み
        
        # GPT-4で回答を取得（最新版の方法）
        openai_response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": user_input}
            ]
        )

        assistant_response = openai_response.choices[0].message.content.strip()
        sources = "外部のOpenAI GPT-4による回答"

    # 履歴タイトル生成（先頭20文字）
    title = user_input if len(user_input) <= 20 else user_input[:20] + '...'

    # 履歴情報を保存（DBに記録）
    history_entry = ChatHistory(
        thread_id=thread_id,
        title=title,
        user_message=user_input,
        assistant_message=assistant_response + "\n\nソース:\n" + sources,
        user_id=current_user.id
    )
    db.session.add(history_entry)
    db.session.commit()

    user_msg_entry = ChatMessage(
        history_id=history_entry.id,
        sender='user',
        message=user_input
    )
    db.session.add(user_msg_entry)

    assistant_msg_entry = ChatMessage(
        history_id=history_entry.id,
        sender='bot',
        message=assistant_response
    )
    db.session.add(assistant_msg_entry)

    db.session.commit()

    return jsonify({
        'thread_id': thread_id,
        'assistant_message': assistant_response,
        'sources': sources
    })

# 履歴一覧ページ表示（ユーザー別に表示）
@app.route('/history', methods=['GET'])
@login_required
def history():
    threads = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.created_at.desc()).all()
    return render_template('history.html', threads=threads)

# 履歴詳細表示ページ
@app.route('/history/<thread_id>')
@login_required
def history_thread(thread_id):
    history = ChatHistory.query.filter_by(thread_id=thread_id, user_id=current_user.id).first_or_404()
    messages = ChatMessage.query.filter_by(history_id=history.id).order_by(ChatMessage.timestamp).all()
    return render_template('chat.html', messages=messages, thread_id=thread_id, title=history.title)

# 履歴メッセージ保存API（新規追加）
@app.route('/save_message', methods=['POST'])
@login_required
def save_message():
    data = request.json
    thread_id = data.get('thread_id')
    content = data['content']
    sender = data['sender']

    history = ChatHistory.query.filter_by(thread_id=thread_id).first()

    if history is None:
        thread_id = thread_id or str(uuid.uuid4())
        title = generate_thread_title(content)
        history = ChatHistory(user_id=current_user.id, thread_id=thread_id, title=title)
        db.session.add(history)
        db.session.commit()

    message = ChatMessage(
        history_id=history.id,
        sender=sender,
        message=content
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({"thread_id": thread_id})

# 履歴削除機能（任意）
@app.route('/history/delete/<thread_id>', methods=['POST'])
@login_required
def delete_history(thread_id):
    history = ChatHistory.query.filter_by(thread_id=thread_id, user_id=current_user.id).first_or_404()
    db.session.delete(history)
    db.session.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
