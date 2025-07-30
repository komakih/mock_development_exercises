from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app.models import User, db, Role, AppConfig
from app.modules.auth.auth import require_permission
from app.modules.admin.forms import CreateUserForm, EditUserForm
from app.modules.logging.security_audit_logger import log_security_event
from app.database import db
from app.modules.logging.log_manager import LogManager
from app.modules.admin.forms import SlackWebhookForm

import logging
from app.modules.utils.slack_log_handler import SlackLogHandler

# セキュリティ監査ロガーの設定（security_audit専用）
security_logger = logging.getLogger('security_audit')
slack_handler = SlackLogHandler()
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
security_logger.addHandler(slack_handler)


# Blueprintを作成（モジュール名を指定）
admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

@admin_bp.route('/users')
@login_required
def user_list():
    if not current_user.has_permission('user_list'):
        flash('ユーザー一覧閲覧権限がありません。', 'warning')
        abort(403)

    users = User.query.all()
    return render_template('admin/user_list.html', users=users)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.has_permission('edit_user'):
        flash('ユーザー編集権限がありません。', 'warning')
        abort(403)

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    all_roles = Role.query.filter(Role.name != 'Admin').all()
    form.role.choices = [(str(r.id), r.name) for r in all_roles]

    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = [str(role.id) for role in user.roles]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        selected_role_ids = [int(rid) for rid in form.role.data]
        selected_roles = Role.query.filter(Role.id.in_(selected_role_ids)).all()
        user.roles = selected_roles
        db.session.commit()

        # セキュリティ監査ログ追加（ユーザー情報更新）
        log_security_event(
            operator_id=current_user.id,
            action="ユーザー情報更新",
            resource_id=user.id,
            details=f"ユーザー{user.email}の情報が更新されました。",
            notify_slack=True
        )

        flash('ユーザー情報を更新しました。', 'success')
        return redirect(url_for('admin.user_list'))

    return render_template('admin/user_edit.html', form=form, user=user)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.has_permission('delete_user'):
        flash('ユーザー削除権限がありません。', 'warning')
        abort(403)

    user = User.query.get_or_404(user_id)
    user_email = user.email
    db.session.delete(user)
    db.session.commit()

    # セキュリティ監査ログ追加（ユーザー削除）
    log_security_event(
        operator_id=current_user.id,
        action="ユーザー削除",
        resource_id=user_id,
        details=f"ユーザー{user_email}を削除しました。",
        notify_slack=True
    )

    flash('ユーザーを削除しました。', 'success')
    return redirect(url_for('admin.user_list'))

@admin_bp.route('/')
@require_permission('create_user')
def admin_index():
    return render_template('admin/user_list.html')

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@require_permission('create_user')
def create_user():
    if not current_user.has_permission('create_user'):
        flash('ユーザー作成権限がありません。', 'warning')
        abort(403)

    form = CreateUserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        # セキュリティ監査ログ追加（ユーザー作成）
        log_security_event(
            operator_id=current_user.id,
            action="ユーザーアカウント作成",
            resource_id=new_user.id,
            details=f"ユーザー{new_user.email}のアカウントを作成しました。",
            notify_slack=True
        )

        flash('新しいユーザーを作成しました。', 'success')
        return redirect(url_for('admin.user_list'))

    return render_template('admin/user_create.html', form=form)

# Slack Webhook設定ページの追加
@admin_bp.route('/slack_webhook', methods=['GET', 'POST'])
@login_required
def slack_webhook():
    form = SlackWebhookForm()

    if request.method == 'GET':
        webhook_url = AppConfig.get_config('SLACK_WEBHOOK_URL')
        if webhook_url:
            form.webhook_url.data = webhook_url

    if form.validate_on_submit():
        AppConfig.set_config('SLACK_WEBHOOK_URL', form.webhook_url.data)
        flash('Slack Webhook URLを更新しました。', 'success')
        return redirect(url_for('admin.slack_webhook'))

    return render_template('admin/slack_webhook.html', form=form)

# ログ参照ページ（メニュー）
@admin_bp.route('/logs')
@login_required
def logs():
    return render_template('admin/log_list.html')

# ベクトル検索失敗ログ表示
@admin_bp.route('/logs/vector_search')
@login_required
def vector_search_logs():
    logs = LogManager.get_logs('vector_search')

    # 特定のクエリを含むログを除外
    filtered_logs = [
        log for log in logs
        if "以下のログを運用チーム向けに簡潔に要約してください" not in log.get('query', '')
    ]

    return render_template('admin/vector_search_log.html', logs=filtered_logs)

# LLM APIリクエストログ表示
@admin_bp.route('/logs/llm_api')
@login_required
def llm_api_logs():
    logs = LogManager.get_logs('llm_api_request')
    return render_template('admin/llm_api_log.html', logs=logs)