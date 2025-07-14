from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.models import User, db
from app.modules.auth.auth import require_permission

# Blueprintを作成（モジュール名を指定）
admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

@admin_bp.route('/users')
@login_required
def user_list():
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

@admin_bp.route('/user/create')
@require_permission('create_user')
def create_user():
    return "ユーザー作成画面"