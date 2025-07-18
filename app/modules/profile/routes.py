from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.forms import ProfileForm
from app.models import db, AppConfig

# Blueprintを作成（モジュール名を指定）
profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def user_profile():
    webhook_url = AppConfig.get_config('SLACK_WEBHOOK_URL') if current_user.is_admin else None

    if request.method == 'POST' and current_user.is_admin:
        new_webhook_url = request.form.get('webhook_url')
        AppConfig.set_config('SLACK_WEBHOOK_URL', new_webhook_url)
        return redirect(url_for('profile.user_profile'))

    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('profile.user_profile'))
    
    return render_template('profile/edit_profile.html', form=form)