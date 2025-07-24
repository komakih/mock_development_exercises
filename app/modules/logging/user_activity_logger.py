import logging
import json
import os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.abspath(os.path.join(basedir, '../../../logs'))
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('user_activity_logger')
logger.setLevel(logging.INFO)

log_file = os.path.join(log_dir, 'user_activity.log')
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)

def log_user_activity(user_id, action, details=None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": int(user_id),
        "action": str(action),
        "details": details if details else ""
    }
    logger.info(json.dumps(log_data, ensure_ascii=False))