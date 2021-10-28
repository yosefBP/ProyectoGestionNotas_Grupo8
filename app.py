#!/usr/bin/python3

from typing import Any
from flask import Flask, render_template, request, redirect, url_for, g, session
from forms import *
from modelos.base_models import selectDb
from modelos.modelUser import Usuarios
from modelos.modelMaterias import Materias
from modelos.modelDocente import Docentes
import yagmail as yag
import functools

# Declaracion e inicializacion de variables
app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = "86272a371c5acfb485b4701c837b922ab6d99134ad679002c36ebb136ad18412"  # SECRET_KEY
mensajeError = "Error: Campo vacio o la informacion solicitada esta incorrecta."


# INICIAR SESION
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view


# Este decorador hace que flask ejecute la funcion definida
# antes de que las peticiones ejecuten la función controladora que solicitan.
@app.before_request
def cargar_usuario_autenticado():
    user_id = session.get('idUsuario')
    if user_id is None:
        g.user = None
    else:
        g.user = Usuarios.get_by_id(user_id)


# LOGOUT
@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    global mensajeError
    errorValidacion1 = "Error: Password o Usuario invalido."
    errorValidacion2 = "Error: Pasword no cumple con criterios de seguridad."
    usuarioLogin = Any

    if request.method == 'GET':
        loginSession = LoginForm()
        return render_template('login.html', form=loginSession)
    else:
        formRequest = LoginForm(request.form)
        if formRequest.validate_on_submit() is True:
            if Usuarios.charValidatorPassword(formRequest.password.data) is True:
                return render_template('login.html', form=formRequest, ErrorValidacion=errorValidacion2)
            usuarioLogin = Usuarios.verificarUsuario(formRequest.e_mail.data, formRequest.password.data)
            if usuarioLogin[0] == 'True':
                session.clear()
                session['idUsuario'] = usuarioLogin[1]
                return redirect(url_for('validacionPolitica'))
            else:
                return render_template('login.html', form=formRequest, ErrorValidacion=errorValidacion1)
        else:
            return render_template('login.html', mensajeError=mensajeError, form=formRequest)


# POLITICA DE PRIVACIDAD
@app.route('/politica/', methods=['GET', 'POST'])
@login_required
def validacionPolitica():
    errorValidacion = "Para finalizar el registro debe marcar la casilla 'ACEPTO LOS TERMINOS' aceptando los terminos de la Politica de Datos"
    formFields = checkboxForm()

    if formFields.validate_on_submit() is True:
        if Usuarios.actualizarPoliticaDatos(formFields.politicaPrivacidad.data, g.user.idUsuario) is True:
            return redirect(url_for('validacionPolitica'))
    elif g.user.politicaPrivacidad == 'N':
        return render_template('politicaDatos.html', mensajeError=errorValidacion, form=formFields)

    if g.user.politicaPrivacidad == 'S':
        if g.user.rol_id == 1:
            return redirect(url_for('infoDocente'))
        elif g.user.rol_id == 2:
            return redirect(url_for('estudianteMaterias'))
        elif g.user.rol_id == 3:
            return redirect(url_for('dashboardAdmin'))


# ADMINISTRADOR
@app.route('/administrador/')
@login_required
def dashboardAdmin():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    return render_template('administrador/home_admin.html')


# ADMINISTRADOR MATERIAS
@app.route('/administrador/gestionar-materias')
@login_required
def adminMaterias():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    materias = Materias.get_all()
    return render_template('administrador/admin_materias.html', listaMaterias=materias)


@app.route('/administrador/crear-materia', methods=['GET', 'POST'])
@login_required
def crearMateria():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = MateriaForm()
        return render_template('administrador/formularios/form_crearMateria.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() is True:
            materiaNueva = Materias(idMateria=formRequest.idMateria.data, nombreMateria=formRequest.nombreMateria.data)
            materiaNueva.insertarMateria()
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_crearMateria.html', mensajeError=mensajeError, form=formRequest)


@app.route('/administrador/editar-materia/<idMateria>', methods=['GET', 'POST'])
@login_required
def editarMateria(idMateria):
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError

    if request.method == 'GET':
        form = MateriaForm()
        materia = Materias.get_by_id(idMateria)
        form.idMateria.data = materia.idMateria
        form.nombreMateria.data = materia.nombreMateria
        return render_template('administrador/formularios/form_editarMateria.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = MateriaForm(request.form)
        if formRequest.validate_on_submit() is True:
            materiaEditada = Materias(idMateria=formRequest.idMateria.data, nombreMateria=formRequest.nombreMateria.data)
            materiaEditada.actualizarMateria()
            return redirect(url_for('adminMaterias'))
        else:
            return render_template('administrador/formularios/form_editarMateria.html', mensajeError=mensajeError, form=formRequest)

@app.route('/administrador/gestionar-materias/eliminar-materia/<idMateria>')
@login_required
def eliminarMateria(idMateria):
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    materia = Materias.get_by_id(idMateria)
    materia.eliminarMateria()
    return redirect(url_for('adminMaterias'))


# ADMINISTRADOR ACTIVIDADES
@app.route('/administrador/gestionar-actividades')
@login_required
def adminActiv():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    return render_template('administrador/admin_actividades.html')


@app.route('/administrar/crear-actividad', methods=['GET', 'POST'])
@login_required
def crearActiv():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_crearActividad.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_crearActividad.html', mensajeError=mensajeError, form=formRequest)


@app.route('/administrar/editar-actividad', methods=['GET', 'POST'])
@login_required
def editarActiv():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = ActividadesForm()
        return render_template('administrador/formularios/form_editarActividad.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = ActividadesForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('adminActiv'))
        else:
            return render_template('administrador/formularios/form_editarActividad.html', mensajeError=mensajeError, form=formRequest)


# ADMINISTRADOR CALIFICACIONES
@app.route('/administrador/calificaciones-y-retroalimentaciones')
@login_required
def indexCalificacion():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    return render_template('administrador/califi_retroalim.html')


@app.route('/administrador/calificar', methods=['GET', 'POST'])
@login_required
def califRetroalim():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_calificar.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_calificar.html', mensajeError=mensajeError, form=formRequest)


@app.route('/administrador/editar-calificacion', methods=['GET', 'POST'])
@login_required
def editCalifRetroalim():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = CalificacionesForm()
        return render_template('administrador/formularios/form_editarCalificacion.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = CalificacionesForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('indexCalificacion'))
        else:
            return render_template('administrador/formularios/form_editarCalificacion.html', mensajeError=mensajeError, form=formRequest)


# ADMINISTRADOR USUARIOS
@app.route('/administrador/gestionar-usuarios')
@login_required
def adminUsuario():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    listaUsuarios = Usuarios.get_all()
    if listaUsuarios:
        return render_template('administrador/admin_usuarios.html', listaUsuarios=listaUsuarios)
    return render_template('administrador/admin_usuarios.html')


@app.route('/adminsistrador/crear-usuarios', methods=['GET', 'POST'])
@login_required
def crearUsuario():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    errorValidacion = ''
    claveEmail = 'Grupo8Ciclo3'
    correoNotificaciones = 'gestornotas2021@gmail.com'

    if request.method == 'GET':
        form = UsuarioForm()
        return render_template('administrador/formularios/form_crearUsuario.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() is True:
            if formRequest.rol_id.data == '':
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
            yagMail = yag.SMTP(correoNotificaciones, claveEmail)
            yagMail.send(to=formRequest.correoUsuario.data, subject="Cuenta de Acceso",
            contents="Bienvenido {0}: \n Ahora eres usuario del Gestor de Notas. \n Usuario: {1} \n Clave de acceso: {2} \n \
             Ingresa a: {3}".format(formRequest.nombreUsuario.data, formRequest.correoUsuario.data, formRequest.password.data, 'https://gestor-de-notas.herokuapp.com/'))
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_crearUsuario.html', mensajeError=mensajeError, form=formRequest)


@app.route('/administrador/editar-usuario/<idUsuario>', methods=['GET', 'POST'])
@login_required
def editarUsuario(idUsuario):
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    errorValidacion = ''
    claveEmail = 'Grupo8Ciclo3'
    correoNotificaciones = 'gestornotas2021@gmail.com'

    if request.method == 'GET':
        form = UsuarioForm()
        usuario = Usuarios.get_by_id(idUsuario)
        form.idUsuario.data = usuario.idUsuario
        form.nombreUsuario.data = usuario.nombreUsuario
        form.apellidoUsuario.data = usuario.apellidoUsuario
        form.correoUsuario.data = usuario.correoUsuario
        form.telefonoUsuario.data = usuario.telefonoUsuario
        form.direccionUsuario.data = usuario.direccionUsuario
        form.password.data = ""
        form.confirmarPassword.data = ""
        form.rol_id.data = str(usuario.rol_id)

        return render_template('administrador/formularios/form_editarUsuario.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = UsuarioForm(request.form)
        if formRequest.validate_on_submit() is True:
            if formRequest.rol_id.data == '':
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
            yagMail = yag.SMTP(correoNotificaciones, claveEmail)
            yagMail.send(to=formRequest.correoUsuario.data, subject="Su mensaje ha sido recibido",
            contents="Hola {0}: \n Ha cambiado tu Password del Gestor de Notas. \n Usuario: {1} \n Nueva Clave de acceso: {2} \n \
             Ingresa a: {3}".format(formRequest.nombreUsuario.data, formRequest.correoUsuario.data, formRequest.password.data, 'https://gestor-de-notas.herokuapp.com/'))
            return redirect(url_for('adminUsuario'))
        elif formRequest.password.data == "" and formRequest.confirmarPassword.data == "":

            usuario = Usuarios(
            idUsuario = formRequest.idUsuario.data,
            nombreUsuario = formRequest.nombreUsuario.data,
            apellidoUsuario = formRequest.apellidoUsuario.data,
            correoUsuario = formRequest.correoUsuario.data,
            telefonoUsuario = formRequest.telefonoUsuario.data,
            direccionUsuario = formRequest.direccionUsuario.data,
            password = "",
            rol_id = int(formRequest.rol_id.data)
            )

            usuario.actualizarUsuario()
            return redirect(url_for('adminUsuario'))
        else:
            return render_template('administrador/formularios/form_editarUsuario.html', mensajeError=mensajeError, form=formRequest)


@app.route('/administrador/gestionar-usuarios/eliminar-usuario/<idUsuario>')
@login_required
def eliminarUsuario(idUsuario):
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    usuario = Usuarios.get_by_id(idUsuario)
    usuario.eliminarUsuario()

    return redirect(url_for('adminUsuario'))


# ADMINISTRADOR DOCENTES
@app.route('/administrador/gestionar-docente')
@login_required
def adminDocente():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    listaDocente = ""
    listaDocentes = Docentes.listaDocentes()

    if listaDocentes:
        return render_template('administrador/admin_docente.html', listaDocentes=listaDocente)
    return render_template('administrador/admin_docente.html.html')


@app.route('/administrador/editar-docente/<idUsuario>', methods=['GET', 'POST'])
def editarDocente():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = DocenteForm()
        return render_template('administrador/formularios/form_editarDocente.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = DocenteForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('adminDocente'))
        else:
            return render_template('administrador/formularios/form_editarDocente.html', mensajeError=mensajeError, form=formRequest)


# ADMINISTRADOR ESTUDIANTES
@app.route('/administrador/gestionar-estudiante')
@login_required
def adminEstudiante():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    return render_template('administrador/admin_estudiante.html')


@app.route('/administrador/editar-estudiante', methods=['GET', 'POST'])
@login_required
def editarEstudiante():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))

    global mensajeError
    if request.method == 'GET':
        form = EstudianteForm()
        return render_template('administrador/formularios/form_editarEstudiante.html', mensajeError=mensajeError, form=form)
    else:
        formRequest = EstudianteForm(request.form)
        if formRequest.validate_on_submit() is True:
            return redirect(url_for('adminEstudiante'))
        else:
            return render_template('administrador/formularios/form_editarEstudiante.html', mensajeError=mensajeError, form=formRequest)


# ADMINISTRADOR INFORMACION PERSONAL
@app.route('/administrador/informacion-personal')
@login_required
def infoAdmin():
    if g.user.rol_id != 3:
        return redirect(url_for('logout'))
    return render_template('administrador/info_admin.html')


# ESTUDIANTE
@app.route('/estudiante')
@login_required
def estudianteMaterias():
    if g.user.rol_id != 2:
        return redirect(url_for('logout'))
    
    materia_usuario = Materias.materiaUsuario(g.user.idUsuario)

    materias = []
    id_materias = []
    
    for n in range(len(materia_usuario)):
        materias.append(materia_usuario[n]['nombreMateria'])
        id_materias.append(materia_usuario[n]['idMateria'])

    return render_template('estudiante/home_estudiante.html', materias = materias, id_materias = id_materias)


@app.route('/estudiante/materia')
@login_required
def materiaActividades():
    if g.user.rol_id != 2:
        return redirect(url_for('logout'))

    id_materia = "id materia"
    num_actividades = [0, 0, 0, 0]
    return render_template('estudiante/materia_actividades.html', id_materia = id_materia, num_actividades = num_actividades)


@app.route('/estudiante/perfil')
@login_required
def estudianteInfoPersonal():
    if g.user.rol_id != 2:
        return redirect(url_for('logout'))

    materia_usuario = Materias.materiaUsuario(g.user.idUsuario)
    notas = Materias.get_notas(g.user.idUsuario)

    promedio = 0.0
    acum = 0.0

    nombre = g.user.nombreUsuario
    apellidos = g.user.apellidoUsuario
    correo = g.user.correoUsuario
    codigo = g.user.idUsuario
    cant_materias = len(materia_usuario)
    for n in range(len(notas)):
        acum = acum + notas[n]['calificacion']
    promedio = round(acum/len(notas),1)

    
    return render_template('estudiante/info_estudiante.html', nombre = nombre, apellidos = apellidos, correo = correo, codigo = codigo, 
                                                                cant_materias = cant_materias, promedio = promedio)


@app.route('/estudiante/resumenNotas')
@login_required
def estudianteNotasOverall():
    if g.user.rol_id != 2:
        return redirect(url_for('logout'))
    materia_usuario = Materias.materiaUsuario(g.user.idUsuario)
    notas_usuario = Materias.get_notas(g.user.idUsuario)
    materias = []
    notas = []
    
    for n in range(len(materia_usuario)):
        materias.append(materia_usuario[n]['nombreMateria'])

    docentes = ['Carlos', 'Juan', 'Laura', 'Vanesa']
    return render_template('estudiante/overallNotas_estudiante.html', materias = materias, notas = notas, docentes = docentes)

# DOCENTE
@app.route('/docente')
@login_required
def infoDocente():
    if g.user.rol_id != 1:
        return redirect(url_for('logout'))

    return render_template('docente/home_docente.html')


@app.route('/docente/registrarActividad')
@login_required
def registrarActividadDocente():
    if g.user.rol_id != 1:
        return redirect(url_for('logout'))

    return render_template('docente/registrarActividad_docente.html')


@app.route('/docente/retroalimentacion')
@login_required
def retroalimentacionDocente():
    if g.user.rol_id != 1:
        return redirect(url_for('logout'))

    return render_template('docente/retroalimentacion_docente.html')