from flask_login import current_user  # 追加
from app.models import Faq
from app.modules.logging.user_activity_logger import log_user_activity  # 追加

def find_similar_questions(user_input, limit=3):
    results = Faq.query.filter(Faq.question.ilike(f'%{user_input}%')).limit(limit).all()

    # FAQ検索時のログ記録を追加
    log_user_activity(current_user.id, action="FAQ検索", details=f"検索内容: {user_input}, 取得件数: {len(results)}")

    return [{"question": faq.question, "answer": faq.answer} for faq in results]
