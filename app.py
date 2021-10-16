from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("Login.html")

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/recuperarcontraseña")
def recuperar_contraseña():
    return render_template('recuperarcontraseña.html')

@app.route("/perfiladmin")
def perfil_admin():
    return render_template('perfiladmin.html')

@app.route("/GestionPilotos")
def Gestion_pilotos():
    return render_template('GestionPilotos.html')

@app.route("/EditarPiloto")
def Editar_pilotos():
    return render_template('EditarPiloto.html')

@app.route("/GestionUsuarios")
def Gestion_Usuarios():
    return render_template('GestionUsuarios.html')

@app.route("/EditarUsuario")
def Editar_Usuarios():
    return render_template('EditarUsuario.html')

@app.route("/GestionVuelos")
def Gestion_Vuelos():
    return render_template('GestionVuelos.html')

@app.route("/CrearVuelos")
def Crear_Vuelos():
    return render_template('CrearVuelos.html')

@app.route("/EditarVuelos")
def Editar_Vuelos():
    return render_template('EditarVuelos.html')



if __name__ == '__main__':
    app.run(debug=True, port=8000)