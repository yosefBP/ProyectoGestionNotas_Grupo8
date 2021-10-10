from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields.core import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import SubmitField
from wtforms.widgets.core import SubmitInput


class LoginForm(FlaskForm):
    e_mail = EmailField('inputEmail', validators=[validators.required()])
    password = PasswordField('inputPassword', validators=[validators.required()])
    btnLogin = SubmitField('Login')