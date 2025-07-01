from fastapi import FastAPI
from api.chat import router as chat_router

app = FastAPI(title="Manual Search AI API")

# APIルーターを登録
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
