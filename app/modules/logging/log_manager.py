import logging
import json
from datetime import datetime
from pytz import timezone as pytz_timezone

# ログ設定
logging.basicConfig(
    filename='logs/login_activity.log',
    level=logging.INFO,
    format='%(message)s'
)

jst = pytz_timezone('Asia/Tokyo')

def log_login_attempt(user_id, email, success, ip_address, user_agent):
    log_data = {
        "timestamp": datetime.now(jst).isoformat(),
        "user_id": user_id,
        "email": email,
        "success": success,
        "ip_address": ip_address,
        "user_agent": user_agent
    }
    logging.info(json.dumps(log_data))

class LogManager:
    LOG_FILES = {
        'vector_search': 'logs/vector_search_activity.log',
        'llm_api_request': 'logs/llm_api_requests.log'
    }

    @staticmethod
    def get_logs(log_type, max_entries=100):
        logfile = LogManager.LOG_FILES.get(log_type)
        if not logfile:
            raise ValueError("無効なログタイプが指定されました。")

        try:
            with open(logfile, 'r', encoding='utf-8') as file:
                lines = file.readlines()[-max_entries:]  # 最新のmax_entries件を取得
                logs = [json.loads(line.strip()) for line in reversed(lines)]
            return logs
        except FileNotFoundError:
            return []

    @staticmethod
    def write_log(log_type, log_data):
        logfile = LogManager.LOG_FILES.get(log_type)
        if not logfile:
            raise ValueError("無効なログタイプが指定されました。")

        log_data['timestamp'] = datetime.now(jst).isoformat()
        with open(logfile, 'a', encoding='utf-8') as file:
            file.write(json.dumps(log_data, ensure_ascii=False) + '\n')