import logging, json, os, traceback
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone

basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.abspath(os.path.join(basedir, '../../../logs'))
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('error_logger')
logger.setLevel(logging.ERROR)

log_file = os.path.join(log_dir, 'error.log')
if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(file_handler)

def log_error(e):
    jst = pytz_timezone('Asia/Tokyo')
    log_data = {
        "timestamp": datetime.now(jst).isoformat(),
        "error_type": type(e).__name__,
        "message": str(e),
        "stack_trace": traceback.format_exc()
    }
    logger.error(json.dumps(log_data, ensure_ascii=False))