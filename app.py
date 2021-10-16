from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    return render_template("registro.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/")
def index():
    return render_template('buscarvuelos1.html')

@app.route("/perfil")
def perfil():
    return render_template('perfilpiloto.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)