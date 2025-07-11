# app/modules/chat/routes.py
from flask import Blueprint, render_template, session, request
from app.openai_utils import get_chatgpt_response
from app.modules.history.history_query import save_chat_history

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
def chat():
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['messages'].append({'role': 'user', 'content': user_input})

        response, source = get_chatgpt_response(session['messages'])
        session['messages'].append({'role': 'assistant', 'content': response})

        # チャット履歴を保存（新しく追加）
        save_chat_history(user_input, response)

    return render_template('chat/index.html', messages=session['messages'])
