from db.database import engine, Base
from db.models import User, ConversationHistory  # モデルを全て明示的にインポート

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ DB初期化完了")

if __name__ == "__main__":
    init_db()
