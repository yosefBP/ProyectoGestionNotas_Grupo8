from flask import Flask, render_template, request
from forms import LoginForm
import os
import yagmail as yag

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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

@app.route('/administrador')
def dashboardAdmin():
    return render_template('administrador/home_admin.html')

@app.route('/administrador/materias')
def adminMaterias():
    return render_template('administrador/materias.html')
