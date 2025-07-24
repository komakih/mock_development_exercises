import logging, json, os
from datetime import datetime
from app.modules.utils.slack_notifier import send_slack_message

import logging
from app.modules.utils.slack_log_handler import SlackLogHandler

# セキュリティ監査ロガーの設定（security_audit専用）
security_logger = logging.getLogger('security_audit')
slack_handler = SlackLogHandler()
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
security_logger.addHandler(slack_handler)

basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.abspath(os.path.join(basedir, '../../../logs'))
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('security_audit_logger')
logger.setLevel(logging.INFO)

log_file = os.path.join(log_dir, 'security_audit.log')
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)

def log_security_event(operator_id, action, resource_id, details=None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "operator_id": int(operator_id),
        "action": action,
        "resource_id": resource_id,
        "details": details if details else ""
    }
    logger.info(json.dumps(log_data, ensure_ascii=False))
    try:
        text = (
            f"✅ セキュリティログ: {action}\n"
            f"📌 実行者: user_id={operator_id}\n"
            f"🔗 対象ID: {resource_id}\n"
            f"📝 詳細: {details}"
        )
        send_slack_message(text)
    except Exception as e:
        print("Slack通知失敗:", e)