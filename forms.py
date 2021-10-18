from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import EmailField, IntegerField, URLField
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
    idUsuario = IntegerField(validators=[validators.required()])
    nombreUsuario = StringField(validators=[validators.required()])
    apellidoUsuario = StringField(validators=[validators.required()])
    correoUsuario = EmailField(validators=[validators.required()])
    telefonoUsuario = IntegerField(validators=[validators.required()])
    direccionUsuario = StringField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])
    confirmarPassword = PasswordField(validators=[validators.required()])
    btnSubmit = SubmitField()

class DocenteForm(FlaskForm):
    idDocente = IntegerField(validators=[validators.required()])
    nombreDocente = StringField(validators=[validators.required()])
    idMateria = IntegerField(validators=[validators.required()])
    nombreMateria = StringField(validators=[validators.required()])
    btnSubmit = SubmitField()

class EstudianteForm(FlaskForm):
    idEstudiante = IntegerField(validators=[validators.required()])
    nombreEstudiante = StringField(validators=[validators.required()])
    idMateria = IntegerField(validators=[validators.required()])
    nombreMateria = StringField(validators=[validators.required()])
    btnSubmit = SubmitField()

class MateriaForm(FlaskForm):
    idMateria = IntegerField(validators=[validators.required()])
    nombreMateria = StringField(validators=[validators.required()])
    btnSubmit = SubmitField()

class ActividadesForm(FlaskForm):
    idMateria = IntegerField(validators=[validators.required()])
    nombreMateria = StringField(validators=[validators.required()])
    idActividad = IntegerField(validators=[validators.required()])
    nombreActividad = StringField(validators=[validators.required()])
    btnSubmit = SubmitField()

class CalificacionesForm(FlaskForm):
    idMateria = IntegerField(validators=[validators.required()])
    nombreMateria = StringField(validators=[validators.required()])
    idActividad = IntegerField(validators=[validators.required()])
    nombreActividad = StringField(validators=[validators.required()])
    idEstudinate = IntegerField(validators=[validators.required()])
    nombreEstudiante = StringField(validators=[validators.required()])
    calificacion = IntegerField(validators=[validators.required()])
    retroalimentacion = StringField(validators=[validators.required()])
    btnSubmit = SubmitField()