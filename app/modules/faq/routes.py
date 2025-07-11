from flask import Blueprint, request, jsonify, render_template
from flask import render_template
from app.modules.faq.faq_query import find_similar_questions
from app.modules.history.history_query import save_chat_history

faq_bp = Blueprint('faq', __name__, template_folder='templates')

@faq_bp.route('/faq-help', methods=['POST'])
def faq_help():
    user_input = request.json.get('message', '')
    similar_questions = find_similar_questions(user_input)
    if similar_questions:
        assistant_message = similar_questions[0]['answer']
    else:
        assistant_message = "関連する情報が見つかりませんでした。"

    save_chat_history(user_input, assistant_message)

    return jsonify({"answer": assistant_message}), 200
    
@faq_bp.route('/chat', methods=['GET'])
def faq_chat():
    return render_template('faq_chat.html')