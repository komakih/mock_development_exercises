# app/modules/chat/routes.py
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.openai_utils import get_chatgpt_response, generate_thread_title
from app.modules.history.history_query import save_chat_history

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    messages = session.get('messages', [])

    if request.method == 'POST':
        if not current_user.has_permission('post_chat'):
            flash('投稿権限がありません。', 'warning')
            abort(403)

        user_input = request.form['user_input']

        # ユーザーメッセージをセッションに追加
        messages.append({'role': 'user', 'content': user_input})

        # OpenAI応答取得処理
        response, source = get_chatgpt_response(messages)
        messages.append({'role': 'assistant', 'content': response})

        # 質問タイトル生成と履歴保存
        title = generate_thread_title(user_input)
        save_chat_history(user_input, response, title=title)

        # セッションを明示的に更新
        session['messages'] = messages
        session.modified = True

    if request.method == 'GET':
        if not current_user.has_permission('view_chat'):
            flash('閲覧権限がありません。', 'warning')
            abort(403)

    return render_template('chat/index.html', messages=messages)

@chat_bp.route('/reset', methods=['POST'])
def reset_chat():
    session.pop('messages', None)
    session.pop('thread_title', None)
    return redirect(url_for('chat.index'))