import logging, json, os
from datetime import datetime
from pytz import timezone as pytz_timezone

# プロジェクトのルートディレクトリを取得
basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.abspath(os.path.join(basedir, '../../../logs'))

# ログディレクトリが存在しない場合は作成
os.makedirs(log_dir, exist_ok=True)

# 専用のロガー作成
logger = logging.getLogger('vector_search_logger')
logger.setLevel(logging.INFO)

logging.basicConfig(
    filename=os.path.join(log_dir, 'vector_search_activity.log'),
    level=logging.INFO,
    format='%(message)s'
)

# ハンドラー（ファイル書き込み）
log_file = os.path.join(log_dir, 'vector_search_activity.log')
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')  # UTF-8エンコード追加
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)

jst = pytz_timezone('Asia/Tokyo')

def log_no_result_search(user_id, query):
    log_data = {
        "timestamp": datetime.now(jst).isoformat(),
        "user_id": user_id,
        "query": query,
        "result": "no_match"
    }
    logging.info(json.dumps(log_data))

def log_search_result(user_id, query, result, similarity, matched):
    log_data = {
        "timestamp": datetime.now(jst).isoformat(),
        "user_id": int(user_id),
        "query": str(query),
        "result": str(result),
        "similarity": float(similarity),
        "matched": bool(matched)
    }
    logger.info(json.dumps(log_data, ensure_ascii=False))