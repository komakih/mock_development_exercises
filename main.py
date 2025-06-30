from fastapi import FastAPI
from api import chat, history, documents, users
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# FastAPIインスタンス作成
app = FastAPI(title="Manual Search AI API", version="1.0")

# 各APIルーターを登録（これから作成予定）
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# トップページ
@app.get("/")
def read_root():
    return {"message": "Welcome to Manual Search AI API"}
