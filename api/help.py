from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

HELP_DIR = "./help"

# ヘルプ情報取得API（ファイル名指定でヘルプ情報を返す）
@router.get("/{filename}")
def get_help_content(filename: str):
    valid_files = {"help": "help.md", "faq": "faq.md"}

    if filename not in valid_files:
        raise HTTPException(status_code=400, detail="無効なヘルプファイル名です。")

    file_path = os.path.join(HELP_DIR, valid_files[filename])

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"filename": valid_files[filename], "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="指定されたヘルプファイルが見つかりません。")
