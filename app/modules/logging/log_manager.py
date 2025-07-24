import logging
import json
from datetime import datetime

# ログ設定
logging.basicConfig(
    filename='logs/login_activity.log',
    level=logging.INFO,
    format='%(message)s'
)

def log_login_attempt(user_id, email, success, ip_address, user_agent):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "email": email,
        "success": success,
        "ip_address": ip_address,
        "user_agent": user_agent
    }
    logging.info(json.dumps(log_data))