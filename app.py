from flask import Flask, render_template, request
from forms import LoginForm
import os
import yagmail as yag

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        loginSession = LoginForm()
        return render_template('login.html', form=loginSession)
    else:
        formRequest = LoginForm(request.form)
        if formRequest.validate_on_submit() == True and formRequest.e_mail.data == 'yosef@gmail.com' :
            return dashboardAdmin()
        elif formRequest.validate_on_submit() == True:
            return '<h1>Success</h1>'
        else:
            return '<h1>Failed</h1>'

# ADMINISTRADOR
@app.route('/administrador')
def dashboardAdmin():
    return render_template('administrador/home_admin.html')

@app.route('/administrador/gestionar-materias')
def adminMaterias():
    return render_template('administrador/admin_materias.html')

@app.route('/administrador/gestionar-actividades')
def adminActiv():
    return render_template('administrador/admin_actividades.html')

@app.route('/administrador/calificaciones-y-retroalimentaciones')
def califRetroalim():
    return render_template('administrador/califi_retroalim.html')

@app.route('/administrador/gestionar-usuarios')
def adminUsuario():
    return render_template('administrador/admin_usuarios.html')

@app.route('/administrador/gestionar-docente')
def adminDocente():
    return render_template('administrador/admin_docente.html')

@app.route('/administrador/gestionar-estudiante')
def adminEstudiante():
    return render_template('administrador/admin_estudiante.html')

@app.route('/administrador/informacion-personal')
def infoAdmin():
    return render_template('administrador/info_admin.html')

# ESTUDIANTE
@app.route('/estudiante')
def estudianteMaterias():
    return render_template('estudiante/home_estudiante.html')

# DOCENTE
