from fastapi import FastAPI
from api import chat, history, documents  # ← 新しくdocumentsを追加

app = FastAPI(title="Manual Search AI API")

# 各APIルーターを登録
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])  # ← 登録追加

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
