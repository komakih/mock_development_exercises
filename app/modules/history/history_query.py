from app.models import ChatHistory

def get_chat_histories(limit=10):
    return ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(limit).all()

def get_chat_history_detail(history_id):
    return ChatHistory.query.get(history_id)