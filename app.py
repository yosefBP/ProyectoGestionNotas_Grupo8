from flask import Flask, render_template, request, redirect, url_for
from forms import *
import os
import yagmail as yag

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
mensajeError = "Error en el campo. Campo vacio o la informacion solicitada esta incorrecta."

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
@app.route('/administrador/')
def dashboardAdmin():
    return render_template('administrador/home_admin.html')

# ADMINISTRADOR MATERIAS
@app.route('/administrador/gestionar-materias')
def adminMaterias():
    return render_template('administrador/admin_materias.html')

@app.route('/administrador/crear-materia', methods=['GET','POST'])
def crearMateria():
    if request.method == 'GET':
        form = MateriaForm()
        return render_template('administrador/formularios/form_crearMateria.html', form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_crearMateria.html', form=formRequest)

@app.route('/administrador/editar-materia', methods=['GET','POST'])
def editarMateria():
    if request.method == 'GET':
        form = MateriaForm()
        return render_template('administrador/formularios/form_editarMateria.html', form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_editarMateria.html', form=formRequest)

# ADMINISTRADOR ACTIVIDADES
@app.route('/administrador/gestionar-actividades')
def adminActiv():
    return render_template('administrador/admin_actividades.html')

@app.route('/administrar/crear-actividad', methods=['GET','POST'])
def crearActiv():
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_crearActividad.html', form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_crearActividad.html', form=formRequest)

@app.route('/administrar/editar-actividad', methods=['GET','POST'])
def editarActiv():
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_editarActividad.html', form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_editarActividad.html', form=formRequest)

# ADMINISTRADOR CALIFICACIONES
@app.route('/administrador/calificaciones-y-retroalimentaciones')
def indexCalificacion():
    return render_template('administrador/califi_retroalim.html')

@app.route('/administrador/calificar', methods=['GET','POST'])
def califRetroalim():
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_calificar.html', form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_calificar.html', form=formRequest)

@app.route('/administrador/editar-calificacion', methods=['GET','POST'])
def editCalifRetroalim():
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_editarCalificacion.html', form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_editarCalificacion.html', form=formRequest)

# ADMINISTRADOR USUARIOS
@app.route('/administrador/gestionar-usuarios')
def adminUsuario():
    return render_template('administrador/admin_usuarios.html')

@app.route('/adminsistrador/crear-usuarios', methods=['GET','POST'])
def crearUsuario():
    global mensajeError
    if request.method == 'GET':
        form = UsuarioForm()
        return render_template('administrador/formularios/form_crearUsuario.html', form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_crearUsuario.html', mensajeError=mensajeError , form=formRequest)

@app.route('/administrador/editar-usuarios', methods=['GET','POST'])
def editarUsuario():
    global mensajeError
    if request.method == 'GET':
        form = UsuarioForm()
        return render_template('administrador/formularios/form_editarUsuario.html', form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_editarUsuario.html', mensajeError=mensajeError, form=formRequest)

# ADMINISTRADOR DOCENTES
@app.route('/administrador/gestionar-docente')
def adminDocente():
    return render_template('administrador/admin_docente.html')

@app.route('/administrador/editar-docente', methods=['GET','POST'])
def editarDocente():
    if request.method == 'GET':
        form = DocenteForm()
        return render_template('administrador/formularios/form_editarDocente.html', form=form)
    else:
        formRequest = DocenteForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminDocente'))
        else:
            return render_template('administrador/formularios/form_editarDocente.html', form=formRequest)

# ADMINISTRADOR ESTUDIANTES
@app.route('/administrador/gestionar-estudiante')
def adminEstudiante():
    return render_template('administrador/admin_estudiante.html')

@app.route('/administrador/editar-estudiante', methods=['GET','POST'])
def editarEstudiante():
    if request.method == 'GET':
        form = EstudianteForm()
        return render_template('administrador/formularios/form_editarEstudiante.html', form=form)
    else:
        formRequest = EstudianteForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminEstudiante'))
        else:
            return render_template('administrador/formularios/form_editarEstudiante.html', form=formRequest)

# ADMINISTRADOR INFORMACION PERSONAL
@app.route('/administrador/informacion-personal')
def infoAdmin():
    return render_template('administrador/info_admin.html')

# ESTUDIANTE
@app.route('/estudiante')
def estudianteMaterias():
    return render_template('estudiante/home_estudiante.html')

@app.route('/estudiante/materia')
def materiaActividades():
    return render_template('estudiante/materia_actividades.html')
# DOCENTE
@app.route('/docente')
def infoDocente():
    return render_template('docente/home_docente.html')
@app.route('/docente/registrarActividad')
def registrarActividadDocente():
    return render_template('docente/registrarActividad_docente.html')
@app.route('/docente/retroalimentacion')
def retroalimentacionDocente():
    return render_template('docente/retroalimentacion_docente.html')