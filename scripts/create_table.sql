-- ユーザーテーブルを作成
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 検索履歴テーブルを作成
CREATE TABLE SearchHistory (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    keyword TEXT NOT NULL,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);

-- 検索結果テーブルを作成
CREATE TABLE SearchResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id INTEGER NOT NULL,
    manual_id TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(history_id) REFERENCES SearchHistory(history_id)
);

-- フィードバックテーブルを作成、現状では未実装予定だけど作っておく
CREATE TABLE Feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    history_id INTEGER,
    user_id INTEGER,
    feedback_type TEXT CHECK(feedback_type IN ('良い', '改善必要')),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(history_id) REFERENCES SearchHistory(history_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);