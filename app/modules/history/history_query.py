from app.database import db
from app.models import ChatHistory
from flask_login import current_user
from app.modules.logging.user_activity_logger import log_user_activity  # 追加
from pytz import timezone as pytz_timezone
from datetime import datetime

def get_chat_histories(limit=10):
    histories = ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    # 履歴閲覧時のログ記録を追加
    log_user_activity(current_user.id, action="履歴一覧閲覧", details=f"取得件数: {limit}")
    return histories

def get_chat_history_detail(history_id):
    history = ChatHistory.query.get(history_id)
    # 履歴詳細閲覧時のログ記録を追加
    log_user_activity(current_user.id, action="履歴詳細閲覧", details=f"履歴ID: {history_id}")
    return history

def save_chat_history(thread_id, user_id, user_message, assistant_message, title=None):
    jst = pytz_timezone('Asia/Tokyo')
    history_entry = ChatHistory(
        thread_id=thread_id,
        user_id=user_id,
        title=title if title else user_message[:20],
        user_message=user_message,
        assistant_message=assistant_message,
        created_at=datetime.now(jst)
    )
    db.session.add(history_entry)
    db.session.commit()
    # 履歴保存時のログ記録を追加
    log_user_activity(current_user.id, action="履歴保存", details=f"タイトル: {history_entry.title}")

def delete_chat_history(history_id):
    history = ChatHistory.query.get(history_id)
    if history:
        db.session.delete(history)
        db.session.commit()
        # 履歴削除時のログ記録を追加
        log_user_activity(current_user.id, action="履歴削除", details=f"履歴ID: {history_id}")
        return True
    return False
