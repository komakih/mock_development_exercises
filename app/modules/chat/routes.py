# app/modules/chat/routes.py
from flask import Blueprint, render_template, session, request, redirect, url_for
from app.openai_utils import get_chatgpt_response, generate_thread_title
from app.modules.history.history_query import save_chat_history

chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
def chat():
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # まずユーザーメッセージをセッションに追加する
        session['messages'].append({'role': 'user', 'content': user_input})

        # 追加後にOpenAIへリクエストする
        response, source = get_chatgpt_response(session['messages'])
        session['messages'].append({'role': 'assistant', 'content': response})

        # 毎回質問ごとに新しいタイトル生成
        title = generate_thread_title(user_input)

        save_chat_history(user_input, response, title=title)

    return render_template('chat/index.html', messages=session['messages'])

@chat_bp.route('/reset', methods=['POST'])
def reset_chat():
    session.pop('messages', None)
    session.pop('thread_title', None)
    return redirect(url_for('chat.chat'))