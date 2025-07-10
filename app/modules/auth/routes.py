from flask import Blueprint, render_template, redirect, url_for
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from app.models import User

# Blueprintを作成（モジュール名を指定）
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('profile.user_profile'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)