from flask import Blueprint, request, jsonify, render_template, json, Response
# from flask_login import login_required, current_user # ← 一旦不要
from . import db
from .models import Prompt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# ログイン無しで動作するバージョンに修正
@main.route('/save_prompt', methods=['POST'])
def save_prompt():
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and Content required'}), 400

    # 仮のuser_idを設定（ログイン無しなら None か固定値を設定）
    new_prompt = Prompt(
        user_id=1, # またはテスト用に仮ID（例:1）
        title=title,
        content=content
    )
    db.session.add(new_prompt)
    db.session.commit()

    return jsonify({'message': 'Prompt saved successfully'}), 201

@main.route('/my_prompts', methods=['GET'])
def my_prompts():
    prompts = Prompt.query.order_by(Prompt.created_at.desc()).all()
    prompts_data = [
        {
            'id': prompt.id,
            'title': prompt.title,
            'content': prompt.content,
            'created_at': prompt.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for prompt in prompts
    ]

    # ここで ensure_ascii=False を設定
    return Response(
        json.dumps(prompts_data, ensure_ascii=False),
        mimetype='application/json'
    )
