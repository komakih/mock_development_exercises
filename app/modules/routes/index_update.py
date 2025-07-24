from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from .index_manager import IndexManager
from app.modules.logging.security_audit_logger import log_security_event

import logging
from app.modules.utils.slack_log_handler import SlackLogHandler

# セキュリティ監査ロガーの設定（security_audit専用）
security_logger = logging.getLogger('security_audit')
slack_handler = SlackLogHandler()
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
security_logger.addHandler(slack_handler)

index_bp = Blueprint('index_update', __name__, template_folder='templates/routes')

@index_bp.route('/update_index', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.has_permission('index_ignite'):
        flash('インデックス更新権限がありません。', 'warning')
        abort(403)

    if request.method == 'POST':
        result = IndexManager.update_index()
        if result['success']:
            # セキュリティ監査ログ追加（インデックス更新成功）
            log_security_event(
                operator_id=current_user.id,
                action="インデックス更新",
                resource_id="index",  # インデックス自体を示す識別子
                details=f"インデックスを更新しました。文書数: {result['document_count']}、所要時間: {result['time']:.2f}秒"
            )
            flash(f"インデックス更新成功！文書数: {result['document_count']}（所要時間: {result['time']:.2f}秒）", "success")
        else:
            # セキュリティ監査ログ追加（インデックス更新失敗）
            log_security_event(
                operator_id=current_user.id,
                action="インデックス更新失敗",
                resource_id="index",
                details=f"インデックス更新に失敗しました: {result['error']}"
            )
            flash(f"インデックス更新失敗: {result['error']}", "error")
        return redirect(url_for('index_update.index'))

    return render_template('routes/index_update.html')
