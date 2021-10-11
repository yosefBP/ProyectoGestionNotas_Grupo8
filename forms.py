from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.fields.simple import SubmitField
from wtforms.widgets.core import CheckboxInput, SubmitInput
from wtforms import validators


class LoginForm(FlaskForm):
    e_mail = EmailField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])
    checkbox = StringField(widget=CheckboxInput())
    submit = SubmitField()