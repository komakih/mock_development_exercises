from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.openai_utils import get_chatgpt_response, generate_thread_title
from app.modules.history.history_query import save_chat_history
from app.modules.rag.rag_utils import perform_vector_search
from app.modules.logging.user_activity_logger import log_user_activity
import uuid
from app.models import db, ChatHistory, AppConfig
import json

chat_bp = Blueprint('chat', __name__, template_folder='templates')

# 曖昧なキーワードを取得するヘルパー関数
def get_ambiguous_keywords():
    config = AppConfig.query.filter_by(config_key="ambiguous_keywords").first()
    if config:
        return json.loads(config.config_value)
    return []

@chat_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())

    thread_id = session['thread_id']
    source_details = None
    form_message = ""

    if request.method == 'POST':
        if not current_user.has_permission('post_chat'):
            flash('投稿権限がありません。', 'warning')
            abort(403)

        user_message = request.form.get('message', '').strip()

        if not user_message:
            flash('質問を入力してください。', 'warning')
            return redirect(url_for('chat.index'))

        # 曖昧キーワードをDBから取得してチェック
        ambiguous_keywords = get_ambiguous_keywords()

        # 曖昧キーワードに該当した場合は専用メッセージを返す（検索処理をスキップ）
        if user_message in ambiguous_keywords:
            assistant_response = "💡 チャットボットの使い方：\n具体的な質問を入力してください\n（例：「商品の配送状況を教えてください」）。"
            source_info = None
        else:
            # 通常の検索処理を行う（曖昧キーワードでない場合）
            assistant_response, source_info = perform_vector_search(current_user.id, user_message)
            if assistant_response is None:
                assistant_response, _ = get_chatgpt_response(current_user.id, [{"role": "user", "content": user_message}])

        title = generate_thread_title(current_user.id, user_message)

        log_user_activity(current_user.id, action="質問送信", details=user_message)
        save_chat_history(thread_id, current_user.id, user_message, assistant_response, title=title)

        source_details = source_info

        return redirect(url_for('chat.index'))

    # 履歴表示の処理（変更なし）
    history_entries = ChatHistory.query.filter_by(thread_id=thread_id, user_id=current_user.id)\
        .order_by(ChatHistory.created_at.asc()).all()

    messages = []
    for entry in history_entries:
        messages.append({"role": "user", "content": entry.user_message})
        messages.append({"role": "assistant", "content": entry.assistant_message})

    return render_template(
        'chat/index.html',
        messages=messages,
        source_details=source_details,
        form_message=form_message
    )

@chat_bp.route('/reset', methods=['POST'])
@login_required
def reset_chat():
    session['thread_id'] = str(uuid.uuid4())
    log_user_activity(current_user.id, action="チャット履歴リセット")

    return redirect(url_for('chat.index'))
