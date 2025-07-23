from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app.modules.logging.log_manager import log_login_attempt
from app.forms import LoginForm, RegisterForm
from app.models import User, db, Role

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
            flash('ログインに成功しました。', 'success')
        else:
            flash('メールアドレスまたはパスワードが正しくありません。', 'danger')

        log_login_attempt(
            user_id=user.id if user else None,
            email=form.email.data,
            success=success,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )

        if success:
            return redirect(url_for('chat.index'))

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
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

        flash('アカウント登録に成功しました。ログインしてください。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)