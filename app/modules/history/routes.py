from flask import Blueprint, render_template, abort
from app.models import ChatHistory
from pytz import timezone
from app.modules.history.history_query import get_chat_histories, get_chat_history_detail

history_bp = Blueprint('history', __name__, template_folder='templates')

@history_bp.route('/histories', methods=['GET'])
def history_list():
    histories = get_chat_histories()
    return render_template('history_list.html', histories=histories)

@history_bp.route('/histories/<int:history_id>', methods=['GET'])
def history_detail(history_id):
    history = get_chat_history_detail(history_id)
    if history is None:
        abort(404)
    return render_template('history_detail.html', history=history)
