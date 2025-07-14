from flask import Blueprint, render_template
import logging

errors_bp = Blueprint('errors', __name__, template_folder='templates')

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    logging.error(f"404 error: {str(e)}")
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    logging.error(f"500 error: {str(e)}")
    return render_template('errors/500.html'), 500