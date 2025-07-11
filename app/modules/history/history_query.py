from app.database import db
from app.models import ChatHistory

def get_chat_histories(limit=10):
    return ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(limit).all()

def get_chat_history_detail(history_id):
    return ChatHistory.query.get(history_id)

def save_chat_history(user_message, assistant_message):
    new_history = ChatHistory(user_message=user_message, assistant_message=assistant_message)
    db.session.add(new_history)
    db.session.commit()