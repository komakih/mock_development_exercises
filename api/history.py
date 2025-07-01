from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import ConversationHistory
from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

router = APIRouter()

# Pydanticスキーマ定義（修正版）
class ConversationCreate(BaseModel):
    user_id: int
    message: str
    response: str

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    response: str
    created_at: datetime

    # Pydantic v2対応（ConfigDictを利用）
    model_config = ConfigDict(from_attributes=True)

# DBセッション依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 履歴登録API（修正版）
@router.post("/", response_model=ConversationResponse)
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    # dict() → model_dump() に変更
    db_conversation = ConversationHistory(**conversation.model_dump())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

# 履歴取得API（ユーザーIDで検索可能）
@router.get("/{user_id}", response_model=List[ConversationResponse])
def get_conversation_history(user_id: int, db: Session = Depends(get_db)):
    conversations = db.query(ConversationHistory).filter_by(user_id=user_id).all()
    if not conversations:
        raise HTTPException(status_code=404, detail="Conversations not found")
    return conversations
