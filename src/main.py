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
    emailOK = collection.find({'usuario' : 'usuario'})
    v = True
    for i in emailOK:
        emailBD = i['email']
        if emailBD == email:
            texto = 'email'
            v = False
            return render_template('index.html', texto = texto)
    if v == True:
        collection_usuario.insert_one({'usuario' : 'usuario', 'nombre' : nombre, 'apellidos' : apellidos, 'email' : email, 'password' : password, 'localidad' : localidad })
        session['email'] = email
        texto = 'Introduzca los datos'
        return redirect(url_for('createCalendario'))
    return render_template('index.html', texto = texto)


@app.route('/login')
def login():
    if 'email' in session:
        return redirect(url_for('createCalendario'))
    return render_template('login.html')


# comprobar el login
@app.route('/login',methods=['POST'])
def comprobar():
    email = request.form.get('email')
    password = request.form.get('contrasena')
    # comprobar en mongoDB si existe ese usuario
    leer_email = list(collection_usuario.find({"usuario" : "usuario", "email" : email}))
    if leer_email != []:
        for i in leer_email:
            if i['email'] == email and i['password'] == password:
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' in session:
        email = session["email"]
        usuario = collection_usuarios.find_one({'email': email})
        id = usuario["_id"]
        calendario = collection.find_one({'usuario' : ObjectId(id)})
        return render_template('home.html', usuario = calendario)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
    # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
