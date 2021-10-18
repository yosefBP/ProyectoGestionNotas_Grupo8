from flask.templating import render_template
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import EmailField, IntegerField, DecimalField
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.widgets.core import CheckboxInput, SubmitInput, TextArea
from wtforms import validators


class LoginForm(FlaskForm):
    e_mail = EmailField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])
    checkbox = StringField(widget=CheckboxInput())
    btnSubmit = SubmitField()

class UsuarioForm(FlaskForm):
    regexEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    rol = SelectField('Rol', choices=[('', 'Elija un Rol'), ('0', 'Docente'), ('1', 'Estudiante'), ('2', 'Administrador')])
    idUsuario = IntegerField('Id Usuario',validators=[validators.required()])
    nombreUsuario = StringField('Nombre',validators=[validators.required()])
    apellidoUsuario = StringField('Apellido',validators=[validators.required()])
    correoUsuario = EmailField('E-mail',validators=[validators.required(), validators.Regexp(regexEmail)])
    telefonoUsuario = IntegerField('Telefono',validators=[validators.required()])
    direccionUsuario = StringField('Direccion',validators=[validators.required()])
    password = StringField('Password',validators=[validators.required()])
    confirmarPassword = StringField('Confirme el password',validators=[validators.required()])
    btnSubmit = SubmitField()

class DocenteForm(FlaskForm):
    idDocente = IntegerField('Id Docente', validators=[validators.required()])
    nombreDocente = StringField('Nombre', validators=[validators.required()])
    idMateria = IntegerField('Id Materia', validators=[validators.required()])
    nombreMateria = StringField('Materia', validators=[validators.required()])
    btnSubmit = SubmitField()

class EstudianteForm(FlaskForm):
    idEstudiante = IntegerField('Id Estudiante', validators=[validators.required()])
    nombreEstudiante = StringField('Nombre', validators=[validators.required()])
    idMateria = IntegerField('Id Materia', validators=[validators.required()])
    nombreMateria = StringField('Materia', validators=[validators.required()])
    btnSubmit = SubmitField()

class MateriaForm(FlaskForm):
    idMateria = IntegerField('Id Materia', validators=[validators.required()])
    nombreMateria = StringField('Nombre', validators=[validators.required()])
    btnSubmit = SubmitField()

class ActividadesForm(FlaskForm):
    idMateria = IntegerField('Id Materia', validators=[validators.required()])
    nombreMateria = StringField('Materia', validators=[validators.required()])
    idActividad = IntegerField('Id Actividad', validators=[validators.required()])
    nombreActividad = TextAreaField('Actividad', validators=[validators.required()])
    btnSubmit = SubmitField()

class CalificacionesForm(FlaskForm):
    idMateria = IntegerField('Id Materia', validators=[validators.required()])
    nombreMateria = StringField('Materia', validators=[validators.required()])
    idActividad = IntegerField('Id Actividad', validators=[validators.required()])
    nombreActividad = StringField('Actividad', validators=[validators.required()])
    idEstudinate = IntegerField('Id Estudiante', validators=[validators.required()])
    nombreEstudiante = StringField('Nombre del Estudiante', validators=[validators.required()])
    calificacion = DecimalField('Calificacion',places=2, validators=[validators.required()])
    retroalimentacion = StringField('Retroalimentacion', validators=[validators.required()])
    btnSubmit = SubmitField()