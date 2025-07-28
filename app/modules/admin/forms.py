from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets
from wtforms.widgets import CheckboxInput
from wtforms.validators import DataRequired, Email, Length
from markupsafe import Markup

class CreateUserForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('ユーザー作成')

class BootstrapCheckboxGroupWidget:
    def __call__(self, field, **kwargs):
        html = ['<div>']
        for subfield in field:
            html.append(
                f'<div class="form-check">'
                f'{subfield(class_="form-check-input")}'
                f'<label class="form-check-label">{subfield.label.text}</label>'
                '</div>'
            )
        html.append('</div>')
        return Markup(''.join(html))

class EditUserForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email()])
    role = SelectMultipleField(
        'ロール',
        choices=[],  # 動的に設定
        option_widget=CheckboxInput(),
        widget=BootstrapCheckboxGroupWidget()
    )
    submit = SubmitField('更新')
