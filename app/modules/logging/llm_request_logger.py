import logging, json, os
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.abspath(os.path.join(basedir, '../../../logs'))
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('llm_request_logger')
logger.setLevel(logging.INFO)

log_file = os.path.join(log_dir, 'llm_request.log')
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)

def log_llm_request(user_id, request_content, response_time, token_count, api_error=None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": int(user_id),
        "request_content": request_content,
        "response_time": float(response_time),
        "token_count": int(token_count),
        "api_error": str(api_error) if api_error else ""
    }
    logger.info(json.dumps(log_data, ensure_ascii=False))