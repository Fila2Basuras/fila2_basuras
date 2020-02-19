from flask import Flask, render_template, redirect, request, url_for, session
from libreria import *
from bson import ObjectId
import os

from pymongo import MongoClient

app = Flask(__name__)


# crear una clave secreta para session
app.secret_key = 'si te metes el dedo en el ojo te duele'


MONGO_URL_ATLAS = 'mongodb+srv://admin:TGTnmlU06H27VEf0@cluster0-6nuch.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['agenda_residuos']
collection = db['calendario']
collection_usuario = db['usuarios']

@app.route('/')
def inicio():
    if 'email' in session:
        return redirect(url_for('createCalendario'))
    texto = 'Rellene los datos del formulario'
    return render_template('index.html', texto = texto)


@app.route('/', methods=['POST'])
def inicioSesion():
    if 'email' in session:
        return redirect(url_for('createCalendario'))
    texto = 'Rellene los datos del formulario'
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    email = request.form.get("email")
    password = request.form.get("contrasena")
    localidad = request.form.get("localidad")
    emailOK = collection_usuario.find({'email' : email})
    v = True
    for i in emailOK:
        emailBD = i['email']
        if emailBD == email:
            texto = 'email'
            v = False
            return render_template('index.html', texto = texto)
    if v == True:
        collection_usuario.insert_one({'nombre' : nombre, 'apellidos' : apellidos, 'email' : email, 'password' : password, 'localidad' : localidad })
        session['email'] = email
        texto = 'Introduzca los datos'
        return redirect(url_for('createCalendario'))
    return render_template('index.html', texto = texto)


@app.route('/login')
def login():
    texto = ""
    if 'email' in session:
        return redirect(url_for('createCalendario'))
    return render_template('login.html', texto=texto)


# comprobar el login
@app.route('/login',methods=['POST'])
def comprobar():
    texto = 'Datos incorrectos'
    email = request.form.get('email')
    password = request.form.get('contrasena')
    # comprobar en mongoDB si existe ese usuario
    leer_email = list(collection_usuario.find({"email" : email}))
    if leer_email != []:
        for i in leer_email:
            if i['email'] == email and i['password'] == password:
                session['email'] = email
                return redirect(url_for('home'))
    return render_template('login.html', texto=texto)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' in session:
        email = session["email"]
        usuario = collection_usuario.find_one({'email': email})
        id = usuario["_id"]
        calendario = collection.find_one({'usuario' : ObjectId(id)}, {'usuario':0, '_id':0 })
        if calendario is None:
            return redirect(url_for('createCalendario'))
        return render_template('home.html', calendario = calendario)
    else:
        return redirect(url_for('inicio'))


@app.route('/calendario/create', methods=('GET', 'POST'))
def createCalendario():
    if 'email' in session:
        email = session["email"]
        usuario = collection_usuario.find_one({'email': email})
        id = usuario["_id"]
        comprobar_tabla = list(collection.find({"usuario" : ObjectId(id)}))
        if comprobar_tabla == []:
            context = {}
            context['semana'] = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
            context['horario_recogida'] = ['mañana', 'tarde', 'noche']
            context['opcion_recogida'] = ['ninguno', 'cristal', 'organicos', 'papel', 'plastico']
            error = None
            if request.method == 'POST':
                calendario = {}

                for value in context['semana']:
                    calendario[value] = {}

                    for horario in context['horario_recogida']:
                    
                        input_name = value + '_' + horario
                        calendario[value][horario] = request.form.get(input_name, '')
                    
                        if calendario[value][horario] not in context['opcion_recogida'] and calendario[value][horario] != '':
                            error = 'Valor no permitido'
                            break
                    if error:
                        break
            
                if not error:
                    #### GUARDAR EN DB
                    calendario['usuario'] = id
                    collection.insert_one(calendario)
                    return redirect(url_for("home"))
        else:
            return redirect(url_for('home'))

        return render_template('calendario/create.html', error=error, context=context)
    else:
        return redirect(url_for('inicio'))

@app.route('/cerrar')
def cerrarSesion():
    session.pop('email',None)
    return render_template('index.html')


if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
    # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
