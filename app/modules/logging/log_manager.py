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