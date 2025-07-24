from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.modules.logging.log_manager import log_login_attempt
from app.modules.logging.security_audit_logger import log_security_event
from app.forms import LoginForm, RegisterForm
from app.models import User, db, Role

import logging
from app.modules.utils.slack_log_handler import SlackLogHandler

# セキュリティ監査ロガーの設定（security_audit専用）
security_logger = logging.getLogger('security_audit')
slack_handler = SlackLogHandler()
slack_handler.setLevel(logging.INFO)
slack_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
security_logger.addHandler(slack_handler)


# Blueprintを作成（モジュール名を指定）
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        success = user and user.check_password(form.password.data)

        if success:
            login_user(user)
            # セキュリティ監査ログ追加（ログイン成功）
            log_security_event(
                operator_id=user.id,
                action="ユーザーログイン",
                resource_id=user.id,
                details=f"ユーザー{user.email}がログインしました。"
            )
            flash('ログインに成功しました。', 'success')
            return redirect(url_for('chat.index'))
        else:
            flash('メールアドレスまたはパスワードが正しくありません。', 'danger')

        log_login_attempt(
            user_id=user.id if user else None,
            email=form.email.data,
            success=success,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    user_id = current_user.id
    email = current_user.email
    logout_user()

    # セキュリティ監査ログ追加（ログアウト成功）
    log_security_event(
        operator_id=user_id,
        action="ユーザーログアウト",
        resource_id=user_id,
        details=f"ユーザー{email}がログアウトしました。"
    )

    flash('ログアウトしました。', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('このメールアドレスは既に登録されています。', 'danger')
            return redirect(url_for('auth.register'))

        # この形でpassword_hashを設定する
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        default_role = Role.query.filter_by(name='User').first()
        if default_role:
            new_user.roles.append(default_role)

        db.session.add(new_user)
        db.session.commit()

        # セキュリティ監査ログ追加（アカウント作成）
        log_security_event(
            operator_id=new_user.id,
            action="ユーザーアカウント作成",
            resource_id=new_user.id,
            details=f"ユーザー{new_user.email}のアカウントが作成されました。"
        )

        flash('アカウント登録に成功しました。ログインしてください。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)