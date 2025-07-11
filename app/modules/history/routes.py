from flask import Blueprint, render_template
from app.models import ChatHistory
from pytz import timezone

history_bp = Blueprint('history', __name__, template_folder='templates')

@history_bp.route('/histories')
def history_list():
    histories = ChatHistory.query.order_by(ChatHistory.created_at.desc()).all()
    return render_template('history_list.html', histories=histories, timezone=timezone)