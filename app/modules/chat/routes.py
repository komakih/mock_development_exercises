from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.openai_utils import get_chatgpt_response, generate_thread_title
from app.modules.history.history_query import save_chat_history
from app.modules.rag.rag_utils import perform_vector_search
from app.modules.logging.vector_search_logger import log_no_result_search
from app.modules.logging.user_activity_logger import log_user_activity  # ←追加
import uuid
from datetime import datetime, timezone
from app.models import db, ChatHistory

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())

    thread_id = session['thread_id']
    source_details = None

    if request.method == 'POST':
        if not current_user.has_permission('post_chat'):
            flash('投稿権限がありません。', 'warning')
            abort(403)

        user_message = request.form.get('message', '').strip()

        if not user_message:
            flash('質問を入力してください。', 'warning')
            return render_template('chat/index.html')

        # LLMまたはRAG検索で回答を取得
        assistant_response, source_info = perform_vector_search(current_user.id, user_message)
        
        if assistant_response is None:
            assistant_response, _ = get_chatgpt_response(current_user.id, [{"role": "user", "content": user_message}])

        # スレッドタイトルを生成（任意）
        title = generate_thread_title(current_user.id, user_message)

        # ユーザー行動ログを記録（質問送信）【再追加】
        log_user_activity(current_user.id, action="質問送信", details=user_message)

        # チャット履歴をデータベースに保存（save_chat_history を再追加）
        save_chat_history(user_message, assistant_response, title=title)

        # ChatHistoryにも履歴を保存（DBでの永続化）
        chat_history_entry = ChatHistory(
            thread_id=thread_id,
            user_id=current_user.id,
            title=title,
            user_message=user_message,
            assistant_message=assistant_response,
            created_at=datetime.now(timezone.utc)
        )
        db.session.add(chat_history_entry)
        db.session.commit()

        source_details = source_info

        return redirect(url_for('chat.index'))

    # DBから履歴を読み込み
    history_entries = ChatHistory.query.filter_by(thread_id=thread_id, user_id=current_user.id).order_by(ChatHistory.created_at.asc()).all()

    messages = []
    for entry in history_entries:
        messages.append({"role": "user", "content": entry.user_message})
        messages.append({"role": "assistant", "content": entry.assistant_message})

    return render_template(
        'chat/index.html',
        messages=messages,
        source_details=source_details
    )

@chat_bp.route('/reset', methods=['POST'])
@login_required
def reset_chat():
    # セッションからスレッドIDを取得し、削除
    thread_id = session.pop('thread_id', None)

    if thread_id:
        # DBから該当スレッドの履歴を全て削除
        ChatHistory.query.filter_by(thread_id=thread_id, user_id=current_user.id).delete()
        db.session.commit()

    # 新しいスレッドIDを再生成（必要に応じて）
    session['thread_id'] = str(uuid.uuid4())

    # ユーザー行動ログを記録（チャット履歴リセット）
    log_user_activity(current_user.id, action="チャット履歴リセット")

    return redirect(url_for('chat.index'))

