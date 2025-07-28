# 模擬開発：社内向け生成AIチャットアプリ

本プロジェクトは、社内業務に生成AI（LLM）を活用するチャットボットアプリケーションの模擬開発演習です。FlaskベースのWebアプリとして実装され、OpenAI API、ChromaDB、LangChainなどを統合しています。

## 🚀 主な機能

- 💬 チャットUI：自然言語による対話形式のチャット
- 🧠 RAG（検索拡張生成）：社内文書に基づく情報検索・回答
- 📚 会話履歴管理：過去のチャットスレッドの保存・再表示
- ❓ ヘルプ＆FAQ：曖昧な入力に対するガイド提示
- 🔐 ユーザー管理：ログイン認証（Flask-Login）
- 🛠️ 管理者画面：FAQの編集やインデックスの更新操作
- 📦 コラボレーションツール連携（予定）

## 🧰 使用技術

- **Python 3.9+**
- **Flask**（Webアプリケーションフレームワーク）
- **OpenAI API**（LLMバックエンド）
- **ChromaDB**（ベクトル検索用データベース）
- **LangChain**（RAG統合フレームワーク）
- **SQLite**（永続化DB）
- **HTML / CSS / JavaScript**（フロントエンド）
- **Flask-Login**（認証管理）

## 📁 ディレクトリ構成（抜粋）

```
mock_development_exercises/
├── run.py                     # アプリ起動スクリプト
├── requirements.txt
└── app/
    ├── __init__.py
    ├── routes.py
    ├── database.py
    ├── chromadb_client.py
    ├── openai_utils.py
    └── modules/
        ├── chat/
        ├── auth/
        ├── admin/
        ├── faq/
        └── errors/
```

## 🔧 セットアップ手順

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt

# アプリ起動
python run.py
```

## 📌 補足

- `.env`ファイルにOpenAI APIキー等の環境変数を設定してください。
- 初期FAQや社内文書は `data/` フォルダに配置します（別途構築）。
- RAGインデックスは自動または手動で再生成可能です。

## 📄 ライセンス

このプロジェクトは模擬開発目的で提供されており、商用利用を意図していません。
