from fastapi import FastAPI, Request
from db.database import engine, Base
from api import chat, history, documents, users, indexing, logs  # logsを追加
from api.utils import setup_error_logger, setup_access_logger

# DBテーブル作成
Base.metadata.create_all(bind=engine)

# ログ設定初期化
error_logger = setup_error_logger()
access_logger = setup_access_logger()

app = FastAPI(title="Manual Search AI API")

# APIルーター登録
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(indexing.router, prefix="/indexing", tags=["Indexing"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])  # 追加

# アクセスログミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    access_logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
