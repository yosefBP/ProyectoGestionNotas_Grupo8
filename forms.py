from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.fields.simple import SubmitField
from wtforms.widgets.core import CheckboxInput, SubmitInput
from wtforms import validators


class LoginForm(FlaskForm):
    e_mail = EmailField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])
    checkbox = StringField(widget=CheckboxInput())
    btnsubmit = SubmitField()

class UsuarioForm(FlaskForm):
    rol = SelectField(choices=[('', 'Elija un Rol'), ('0', 'Docente'), ('1', 'Estudiante'), ('2', 'Administrador')])
    btnSubmit = SubmitField()

class DocenteForm(FlaskForm):
    btnSubmit = SubmitField()

class EstudianteForm(FlaskForm):
    btnSubmit = SubmitField()

class MateriaForm(FlaskForm):
    btnSubmit = SubmitField()

class ActividadesForm(FlaskForm):
    btnSubmit = SubmitField()

class CalificacionesForm(FlaskForm):
    btnSubmit = SubmitField()