import logging, json, os
from datetime import datetime

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