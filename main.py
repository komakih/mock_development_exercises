from fastapi import FastAPI
from db.database import engine, Base
from api import chat, history, documents, users, indexing  # indexingを追加

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Manual Search AI API")

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(indexing.router, prefix="/indexing", tags=["Indexing"])  # indexing追加

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}
