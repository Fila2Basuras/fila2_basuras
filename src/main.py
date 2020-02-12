from flask import Flask, render_template, redirect, request, url_for
from libreria import *
import os

from pymongo import MongoClient

app = Flask(__name__)

MONGO_URL_ATLAS = 'mongodb+srv://admin:TGTnmlU06H27VEf0@cluster0-6nuch.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(MONGO_URL_ATLAS, ssl_cert_reqs=False)
db = client['agenda_residuos']
collection = db['calendario']

@app.route('/', methods=['GET', 'POST'])
def index():
    ejemplo = list(collection.find({}))
    return render_template('index.html', ejemplo=ejemplo)


if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
    # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
