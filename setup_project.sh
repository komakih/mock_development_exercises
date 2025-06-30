#!/bin/bash

# プロジェクト構造作成スクリプト

# ディレクトリを作成
mkdir -p manual_db documents db api tests scripts

echo "✅ ディレクトリ作成完了"

# 空ファイル作成（touchコマンド）
touch .env requirements.txt main.py
touch db/database.py db/models.py
touch api/__init__.py api/chat.py api/history.py api/documents.py api/users.py api/utils.py
touch tests/test_api.py
touch scripts/import_to_chromadb.py scripts/query_chromadb.py

echo "✅ ファイル作成完了"

# 作成結果の表示
echo "📂 作成したディレクトリとファイル:"
tree . -I "myenv|__pycache__"

