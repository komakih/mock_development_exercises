from app.database import db
from app.models import ChatHistory
from app.openai_utils import generate_thread_title

def get_chat_histories(limit=10):
    return ChatHistory.query.order_by(ChatHistory.created_at.desc()).limit(limit).all()

def get_chat_history_detail(history_id):
    return ChatHistory.query.get(history_id)

def save_chat_history(user_message, assistant_message):
    new_history = ChatHistory(user_message=user_message, assistant_message=assistant_message)
    db.session.add(new_history)
    db.session.commit()

def delete_chat_history(history_id):
    history = ChatHistory.query.get(history_id)
    if history:
        db.session.delete(history)
        db.session.commit()
        return True
    return False

def save_chat_history(user_message, assistant_message, user_id=None):
    title = generate_thread_title(user_message)
    new_history = ChatHistory(
        user_message=user_message,
        assistant_message=assistant_message,
        user_id=user_id,
        title=title
    )
    db.session.add(new_history)
    db.session.commit()