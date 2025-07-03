from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

LOG_DIR = "./logs"

# 指定したログファイルを取得するAPI
@router.get("/{log_type}")
def get_logs(log_type: str):
    valid_logs = {"error": "error.log", "access": "access.log"}

    if log_type not in valid_logs:
        raise HTTPException(status_code=400, detail="Invalid log type")

    log_file_path = os.path.join(LOG_DIR, valid_logs[log_type])

    try:
        with open(log_file_path, "r") as log_file:
            content = log_file.read()
        return {"log_type": log_type, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
