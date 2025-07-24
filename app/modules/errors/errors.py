from flask import Blueprint, render_template
from app.modules.logging.error_logger import log_error  # 追加

errors_bp = Blueprint('errors', __name__, template_folder='templates')

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    log_error(e)  # ログ記録を追加
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    log_error(e)  # ログ記録を追加
    return render_template('errors/500.html'), 500
