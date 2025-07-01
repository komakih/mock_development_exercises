from fastapi import FastAPI
from db.database import engine, Base
from api import chat, history

# SQLiteテーブルを初期化（モデルに基づいてDB作成）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manual Search AI API")

# ルーターの登録
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
