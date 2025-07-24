from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.modules.history.history_query import (
    get_chat_histories, get_chat_history_detail, delete_chat_history
)
from app.modules.logging.security_audit_logger import log_security_event

import logging
from app.modules.utils.slack_log_handler import SlackLogHandler

# セキュリティ監査ロガーの設定（security_audit専用）
security_logger = logging.getLogger('security_audit')
slack_handler = SlackLogHandler()
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
security_logger.addHandler(slack_handler)

history_bp = Blueprint('history', __name__, template_folder='templates')

@history_bp.route('/histories', methods=['GET'])
@login_required
def history_list():
    if not current_user.has_permission('view_history'):
        flash('履歴閲覧権限がありません。', 'warning')
        abort(403)

    histories = get_chat_histories()
    return render_template('history/history_list.html', histories=histories)

@history_bp.route('/histories/<int:history_id>', methods=['GET'])
@login_required
def history_detail(history_id):
    if not current_user.has_permission('view_history'):
        flash('履歴閲覧権限がありません。', 'warning')
        abort(403)

    history = get_chat_history_detail(history_id)
    if history is None:
        abort(404)
    return render_template('history/history_detail.html', history=history)

@history_bp.route('/histories/delete/<int:history_id>', methods=['POST'])
@login_required
def history_delete(history_id):
    if not current_user.has_permission('delete_history'):
        flash('履歴削除権限がありません。', 'warning')
        abort(403)

    delete_chat_history(history_id)

    # セキュリティ監査ログ追加（履歴削除）
    log_security_event(
        operator_id=current_user.id,
        action="履歴削除",
        resource_id=history_id,
        details=f"ユーザー{current_user.email}が履歴{history_id}を削除しました。"
    )

    flash('履歴を削除しました。', 'success')
    return redirect(url_for('history.history_list'))
