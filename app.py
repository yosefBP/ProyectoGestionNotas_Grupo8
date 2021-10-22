from flask import Flask, render_template, request, redirect, url_for
from forms import *
from modelos.classModels import Usuarios
import os
import yagmail as yag

app = Flask(__name__)
#SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = "86272a371c5acfb485b4701c837b922ab6d99134ad679002c36ebb136ad18412" #SECRET_KEY
mensajeError = "Error en el campo. Campo vacio o la informacion solicitada esta incorrecta."

# LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    global mensajeError
    mensajeError1 = "Error. Campo vacio o el Usuario es invalido."
    mensajeError2 = "Error. Campo vacio o el Password es invalido."
    mensajeError3 = "Error. Campo vacio."
    if request.method == 'GET':
        loginSession = LoginForm()
        return render_template('login.html', form=loginSession)
    else:
        formRequest = LoginForm(request.form)
        if formRequest.validate_on_submit() == True:
            return '<h1>Success</h1>'
        else:
            if formRequest.e_mail.data == "" and formRequest.password.data == "":
                return render_template('login.html', form=formRequest, mensajeError=mensajeError3)
            elif formRequest.e_mail.data == "" and formRequest.password.data != "":
                return render_template('login.html', form=formRequest, mensajeError=mensajeError1)
            elif formRequest.password.data == "" and formRequest.e_mail.data != "":
                return render_template('login.html', mensajeError=mensajeError2, form=formRequest)
            else:
                return render_template('login.html', mensajeError=mensajeError, form=formRequest)

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
    global mensajeError
    if request.method == 'GET':
        form = MateriaForm()
        return render_template('administrador/formularios/form_crearMateria.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_crearMateria.html', mensajeError=mensajeError, form=formRequest)

@app.route('/administrador/editar-materia', methods=['GET','POST'])
def editarMateria():
    global mensajeError
    if request.method == 'GET':
        form = MateriaForm()
        return render_template('administrador/formularios/form_editarMateria.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_editarMateria.html', mensajeError=mensajeError, form=formRequest)

# ADMINISTRADOR ACTIVIDADES
@app.route('/administrador/gestionar-actividades')
def adminActiv():
    return render_template('administrador/admin_actividades.html')

@app.route('/administrar/crear-actividad', methods=['GET','POST'])
def crearActiv():
    global mensajeError
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_crearActividad.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_crearActividad.html', mensajeError=mensajeError, form=formRequest)

@app.route('/administrar/editar-actividad', methods=['GET','POST'])
def editarActiv():
    global mensajeError
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_editarActividad.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_editarActividad.html', mensajeError=mensajeError, form=formRequest)

# ADMINISTRADOR CALIFICACIONES
@app.route('/administrador/calificaciones-y-retroalimentaciones')
def indexCalificacion():
    return render_template('administrador/califi_retroalim.html')

@app.route('/administrador/calificar', methods=['GET','POST'])
def califRetroalim():
    global mensajeError
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_calificar.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_calificar.html', mensajeError=mensajeError, form=formRequest)

@app.route('/administrador/editar-calificacion', methods=['GET','POST'])
def editCalifRetroalim():
    global mensajeError
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_editarCalificacion.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_editarCalificacion.html', mensajeError=mensajeError, form=formRequest)

# ADMINISTRADOR USUARIOS
@app.route('/administrador/gestionar-usuarios')
def adminUsuario():
    listaUsuarios = Usuarios.get_all()
    if listaUsuarios:
        return render_template('administrador/admin_usuarios.html', listaUsuarios=listaUsuarios)
    return render_template('administrador/admin_usuarios.html')

@app.route('/adminsistrador/crear-usuarios', methods=['GET','POST'])
def crearUsuario():
    global mensajeError
    errorValidacion = ''

    if request.method == 'GET':
        form = UsuarioForm()
        return render_template('administrador/formularios/form_crearUsuario.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() == True :
            if formRequest.rol_id.data == '' :
                errorValidacion = 'Seleccione un Rol'
                return render_template('administrador/formularios/form_crearUsuario.html', 
                ErrorValidacion=errorValidacion, form=formRequest)
            if formRequest.password.data != formRequest.confirmarPassword.data:
                errorValidacion = 'Las contraseñas no coinciden'
                return render_template('administrador/formularios/form_crearUsuario.html', 
                ErrorValidacion=errorValidacion, form=formRequest)

            nuevoUsuario = Usuarios(formRequest.idUsuario.data, formRequest.nombreUsuario.data, formRequest.apellidoUsuario.data, 
            formRequest.correoUsuario.data, formRequest.telefonoUsuario.data, formRequest.direccionUsuario.data, formRequest.password.data, int(formRequest.rol_id.data))

            nuevoUsuario.insertarUsuario()
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_crearUsuario.html', mensajeError=mensajeError , form=formRequest)

@app.route('/administrador/editar-usuario<idUsuario>', methods=['GET','POST'])
def editarUsuario(idUsuario):
    global mensajeError
    errorValidacion = ''

    if request.method == 'GET':
        form = UsuarioForm()
        usuario = Usuarios.get_by_id(idUsuario)
        form.idUsuario.data = usuario.idUsuario
        form.nombreUsuario.data = usuario.nombreUsuario
        form.apellidoUsuario.data = usuario.apellidoUsuario
        form.correoUsuario.data = usuario.correoUsuario
        form.telefonoUsuario.data = usuario.telefonoUsuario
        form.direccionUsuario.data = usuario.direccionUsuario
        form.password.data = usuario.password
        form.confirmarPassword.data = usuario.password
        form.rol_id.data = str(usuario.rol_id)

        return render_template('administrador/formularios/form_editarUsuario.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() == True :
            if formRequest.rol_id.data == '' :
                errorValidacion = 'Seleccione un Rol'
                return render_template('administrador/formularios/form_editarUsuario.html', 
                ErrorValidacion=errorValidacion, form=formRequest)
            if formRequest.password.data != formRequest.confirmarPassword.data:
                errorValidacion = 'Las contraseñas no coinciden'
                return render_template('administrador/formularios/form_editarUsuario.html', 
                ErrorValidacion=errorValidacion, form=formRequest)

            usuario = Usuarios(
            idUsuario = formRequest.idUsuario.data,
            nombreUsuario = formRequest.nombreUsuario.data,
            apellidoUsuario = formRequest.apellidoUsuario.data,
            correoUsuario = formRequest.correoUsuario.data,
            telefonoUsuario = formRequest.telefonoUsuario.data,
            direccionUsuario = formRequest.direccionUsuario.data,
            password = formRequest.password.data,
            rol_id = int(formRequest.rol_id.data)
            )

            usuario.actualizarUsuario()
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_editarUsuario.html', mensajeError=mensajeError, form=formRequest)

@app.route('/administrador/gestionar-usuarios/eliminar-usuario<idUsuario>')
def eliminarUsuario(idUsuario):
    usuario = Usuarios.get_by_id(idUsuario)
    usuario.eliminarUsuario()

    return redirect(url_for('adminUsuario'))

# ADMINISTRADOR DOCENTES
@app.route('/administrador/gestionar-docente')
def adminDocente():
    return render_template('administrador/admin_docente.html')

@app.route('/administrador/editar-docente', methods=['GET','POST'])
def editarDocente():
    global mensajeError
    if request.method == 'GET':
        form = DocenteForm()
        return render_template('administrador/formularios/form_editarDocente.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = DocenteForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminDocente'))
        else:
            return render_template('administrador/formularios/form_editarDocente.html', mensajeError=mensajeError, form=formRequest)

# ADMINISTRADOR ESTUDIANTES
@app.route('/administrador/gestionar-estudiante')
def adminEstudiante():
    return render_template('administrador/admin_estudiante.html')

@app.route('/administrador/editar-estudiante', methods=['GET','POST'])
def editarEstudiante():
    global mensajeError
    if request.method == 'GET':
        form = EstudianteForm()
        return render_template('administrador/formularios/form_editarEstudiante.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = EstudianteForm(request.form)
        if formRequest.validate_on_submit() == True:
            return redirect(url_for('adminEstudiante'))
        else:
            return render_template('administrador/formularios/form_editarEstudiante.html', mensajeError=mensajeError, form=formRequest)

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

@app.route('/estudiante/perfil')
def estudianteInfoPersonal():
    return render_template('estudiante/info_estudiante.html')

@app.route('/estudiante/resumenNotas')
def estudianteNotasOverall():
    return render_template('estudiante/overallNotas_estudiante.html')

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