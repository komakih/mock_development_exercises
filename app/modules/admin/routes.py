from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app.models import User, db
from app.modules.auth.auth import require_permission
from app.modules.admin.forms import CreateUserForm
from app.database import db

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
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        return redirect(url_for('admin.user_list'))
    return render_template('admin/user_edit.html', user=user)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.user_list'))

@admin_bp.route('/')
@require_permission('create_user')
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@require_permission('create_user')
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('新しいユーザーを作成しました。', 'success')
        return redirect(url_for('admin.admin_index'))

    return render_template('admin/user_create.html', form=form)