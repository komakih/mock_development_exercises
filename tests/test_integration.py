import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import SessionLocal, Base, engine
from db.models import User, ConversationHistory

client = TestClient(app)

# DBを毎回クリーンに初期化するfixtureを作成
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    # テーブルを完全に削除して再作成（毎回テスト前にDBを初期化）
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # fixture実行後にyieldでテスト実行
    yield

    # 後処理（通常は不要だが、必要なら追加可能）

# 統合テスト
def test_user_flow():
    # ユーザー登録
    signup_response = client.post("/users/signup", json={
        "username": "integration_test_user",
        "password": "integration_test_pass"
    })
    assert signup_response.status_code == 200
    user_data = signup_response.json()
    user_id = user_data["id"]

    # ログイン（JWT取得）
    login_response = client.post("/users/login", json={
        "username": "integration_test_user",
        "password": "integration_test_pass"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # チャットAPIを実行（履歴が自動保存される）
    chat_response = client.post("/chat/query", params={
        "message": "返品方法を教えてください",
        "user_id": user_id  # ここを必ず追加（ユーザーIDを指定）
    })
    assert chat_response.status_code == 200

    # 会話履歴を取得（自動で保存されていることを確認）
    history_response = client.get(f"/history/{user_id}")
    assert history_response.status_code == 200
    history_data = history_response.json()
    assert len(history_data) > 0
    assert history_data[0]["message"] == "返品方法を教えてください"

    # ドキュメント検索APIテスト
    doc_search_response = client.post("/documents/search", json={"query_text": "返品方法", "n_results": 2})
    assert doc_search_response.status_code == 200
    doc_data = doc_search_response.json()
    assert len(doc_data["results"]) > 0

    # インデックス更新APIテスト
    indexing_response = client.post("/indexing/update")
    assert indexing_response.status_code == 200

    # ログ取得APIテスト（エラーとアクセスログ）
    error_log_response = client.get("/logs/error")
    assert error_log_response.status_code == 200

    access_log_response = client.get("/logs/access")
    assert access_log_response.status_code == 200

    # ヘルプAPIテスト
    help_response = client.get("/help/help")
    assert help_response.status_code == 200
