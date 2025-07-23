from flask import Blueprint, request, jsonify, render_template, abort, flash, session
from flask_login import login_required, current_user
from app.modules.faq.faq_query import find_similar_questions
from app.modules.history.history_query import save_chat_history

faq_bp = Blueprint('faq', __name__, template_folder='templates')

@faq_bp.route('/faq-help', methods=['GET', 'POST'])
@login_required
def faq_help():
    if not current_user.has_permission('view_document'):
        flash('FAQ閲覧権限がありません。', 'warning')
        abort(403)

    if 'faq_messages' not in session:
        session['faq_messages'] = []

    if request.method == 'POST':
        user_input = request.json.get('message', '')
        similar_questions = find_similar_questions(user_input)

        if similar_questions:
            assistant_message = similar_questions[0]['answer']
        else:
            assistant_message = "関連する情報が見つかりませんでした。"

        session['faq_messages'].append({'role': 'user', 'content': user_input})
        session['faq_messages'].append({'role': 'assistant', 'content': assistant_message})
        session.modified = True

        save_chat_history(user_input, assistant_message)

        return jsonify({"answer": assistant_message}), 200

    return render_template('faq/faq_chat.html', messages=session['faq_messages'])

@faq_bp.route('/faq-reset', methods=['POST'])
@login_required
def reset_faq_chat():
    session.pop('faq_messages', None)
    flash('チャット履歴をリセットしました。', 'info')
    return jsonify({'status': 'success'}), 200