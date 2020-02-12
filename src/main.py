from flask import Flask, render_template, redirect, request, url_for
from libreria import *
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # Esto es un problema porque no le podemos poner un puerto de salida, para eso vamos a crear lo siguiente:
    # SI HAY VARIABLE DE ENTORNO PORT COJE ESA VARIABLE, SI NO COJE EL 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
