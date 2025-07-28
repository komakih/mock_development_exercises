from flask import Blueprint, request, jsonify, render_template, abort, flash, session
from flask_login import login_required, current_user
from app.modules.faq.faq_query import find_similar_questions
from app.modules.history.history_query import save_chat_history
from app.models import db, ChatHistory

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

        # FAQ用に固定のthread_id（例: 0）を使用する
        faq_thread_id = 0
        save_chat_history(faq_thread_id, current_user.id, user_input, assistant_message)

        return jsonify({"answer": assistant_message}), 200

    return render_template('faq/faq_chat.html', messages=session['faq_messages'])

@faq_bp.route('/faq-reset', methods=['POST'])
@login_required
def reset_faq_chat():
    faq_thread_id = 0  # FAQ専用のthread_idを指定

    try:
        # DBから該当のFAQ履歴を削除
        ChatHistory.query.filter_by(
            thread_id=faq_thread_id,
            user_id=current_user.id
        ).delete()

        db.session.commit()

        # sessionもクリア（オプション）
        session.pop('faq_messages', None)

        flash('FAQチャット履歴をリセットしました。', 'info')
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        db.session.rollback()
        flash('FAQ履歴のリセットに失敗しました。', 'danger')
        return jsonify({'status': 'error', 'message': str(e)}), 500