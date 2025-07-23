# app/modules/chat/routes.py
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.openai_utils import get_chatgpt_response, generate_thread_title
from app.modules.history.history_query import save_chat_history
from app.modules.rag.rag_utils import perform_vector_search
from app.modules.logging.vector_search_logger import log_no_result_search

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if 'messages' not in session:
        session['messages'] = []

    user_message = None
    assistant_response = None
    source_details = None

    if request.method == 'POST':
        if not current_user.has_permission('post_chat'):
            flash('投稿権限がありません。', 'warning')
            abort(403)

        user_message = request.form.get('message', '').strip()

        if not user_message:
            flash('質問を入力してください。', 'warning')
            return render_template('chat/index.html', user_message=None, assistant_response=None)

        session['messages'].append({'role': 'user', 'content': user_message})

        rag_response, source_info = perform_vector_search(current_user.id, user_message)

        if rag_response:
            assistant_response = rag_response
            source_details = source_info
        else:
            assistant_response, source = get_chatgpt_response(session['messages'])
            log_no_result_search(current_user.id, user_message)
            source_details = None

        session['messages'].append({'role': 'assistant', 'content': assistant_response})

        title = generate_thread_title(user_message)
        save_chat_history(user_message, assistant_response, title=title)

        session.modified = True

    return render_template(
    'chat/index.html', 
    user_message=user_message,
    assistant_response=assistant_response,
    source_details=source_details
    )

@chat_bp.route('/reset', methods=['POST'])
def reset_chat():
    session.pop('messages', None)
    session.pop('thread_title', None)
    return redirect(url_for('chat.index'))