import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import engine, Base
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    # テスト前の準備：DB初期化
    Base.metadata.drop_all(bind=engine)  # DBを一度クリア
    Base.metadata.create_all(bind=engine)  # 再作成
    yield
    # テスト後の処理（何もしなくてもよいが、必要ならここで処理）

def test_user_signup_and_login():
    # ユーザー登録テスト
    response = client.post("/users/signup", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

    # ログインテスト
    response = client.post("/users/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    login_data = response.json()
    assert "access_token" in login_data

def test_user_deletion():
    # テストユーザーを作成
    signup_response = client.post("/users/signup", json={
        "username": "deleteuser",
        "password": "deletepassword"
    })
    assert signup_response.status_code == 200
    user_data = signup_response.json()
    user_id = user_data["id"]

    # ユーザー削除テスト
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["detail"] == "ユーザーが正常に削除されました"

    # 削除されたユーザーが存在しないことを確認
    users_response = client.get("/users/")
    users_list = users_response.json()
    assert all(user["id"] != user_id for user in users_list)

def test_index_update():
    response = client.post("/indexing/update")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "インデックス更新完了"

def test_get_logs():
    # エラーログ取得テスト
    response = client.get("/logs/error")
    assert response.status_code == 200
    data = response.json()
    assert "content" in data

    # アクセスログ取得テスト
    response = client.get("/logs/access")
    assert response.status_code == 200
    data = response.json()
    assert "content" in data

    # 存在しないログタイプのテスト
    response = client.get("/logs/invalid")
    assert response.status_code == 400
