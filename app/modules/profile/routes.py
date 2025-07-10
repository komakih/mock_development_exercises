from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.forms import ProfileForm
from app.models import db

# Blueprintを作成（モジュール名を指定）
profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('profile.user_profile'))
    return render_template('profile/edit_profile.html', form=form)