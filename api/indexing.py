from fastapi import APIRouter, HTTPException
from scripts.indexing import rebuild_chromadb_index

router = APIRouter()

# インデックス更新API（管理者用）
@router.post("/update")
def update_index():
    result = rebuild_chromadb_index()
    if result["status"] == "success":
        return {"detail": result["message"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])
