from flask import Blueprint, request, jsonify, render_template
from flask import render_template
from app.modules.faq.faq_query import find_similar_questions

faq_bp = Blueprint('faq', __name__, template_folder='templates')

@faq_bp.route('/faq-help', methods=['POST'])
def faq_help():
    user_input = request.json.get('message', '')
    similar_questions = find_similar_questions(user_input)
    if similar_questions:
        return jsonify({"suggestions": similar_questions}), 200
    else:
        return jsonify({"suggestions": ["関連する情報が見つかりませんでした。"]}), 200
    
@faq_bp.route('/chat', methods=['GET'])
def faq_chat():
    return render_template('faq_chat.html')