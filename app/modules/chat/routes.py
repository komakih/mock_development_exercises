# app/modules/chat/routes.py
from flask import Blueprint, render_template, session, request
from app.openai_utils import get_chatgpt_response


chat_bp = Blueprint('chat', __name__, template_folder='templates')

@chat_bp.route('/', methods=['GET', 'POST'])
def index():
    if 'messages' not in session:
        session['messages'] = []

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['messages'].append({'role': 'user', 'content': user_input})
        
        response, source = get_chatgpt_response(session['messages'])
        session['messages'].append({'role': 'assistant', 'content': response, 'source': source})
    
    return render_template('chat/index.html', messages=session['messages'])
