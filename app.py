from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os
import sqlite3
from sqlite3 import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# @app.route("/")
# def inicio():
#     return render_template("Login.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("Login.html")
    
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        tipoPerfil = "Administrador"
        try:
            with sqlite3.connect('Plavue.db') as con: 
             cur = con.cursor()
             cur.execute("SELECT * FROM Usuarios WHERE correo=? AND contraseña =? AND tipoPerfil=?",[correo,password, tipoPerfil])
             if cur.fetchone():
                 return render_template("perfiladmin.html")
             elif request.method == "POST":
                 correo = request.form["correo"]
                 password = request.form["password"]
                 tipoPerfil = "Piloto"
                 try:
                    with sqlite3.connect('Plavue.db') as con: 
                     cur = con.cursor()
                     cur.execute("SELECT * FROM Usuarios WHERE correo=? AND contraseña =? AND tipoPerfil=?",[correo,password, tipoPerfil])
                     if cur.fetchone():
                         return render_template("perfilpiloto.html")
                     elif request.method == "POST":
                        correo = request.form["correo"]
                        password = request.form["password"]
                        try:
                            with sqlite3.connect('Plavue.db') as con: 
                             cur = con.cursor()
                             cur.execute("SELECT * FROM Usuarios WHERE correo=? AND contraseña =?",[correo,password])
                             if cur.fetchone():
                                return render_template("perfilusuario.html")
                             else:
                                return "Usuario no permitido"
                        except Error as er:
                            print('SQLite error: %s' % (' '.join(er.args)))
                            print('SQLite traceback: ')
                 except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ')
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print('SQLite traceback: ')
    return render_template("Login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    now = datetime.now()
    id = now.strftime("%Y%m%d%H%M%S")
    print(id)
    if request.method == 'POST':
        now = datetime.now()
        id = now.strftime("%Y%m%d%H%M%S")
        nombre = request.form["Nombre"]
        correo = request.form["correo"]
        password = request.form["password"]        
        try:
            with sqlite3.connect('Plavue.db') as con: #establecer objeto conexion a base de datos
                cur = con.cursor() #manipular la conexión a la bd
                cur.execute('INSERT INTO Usuarios (idUsuario, contraseña, Nombre, correo) VALUES (?,?,?,?)', (id, password, nombre,correo))
                con.commit() #confirmar la transacción
                return render_template("Login.html")
        except Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print('SQLite traceback: ')
            return "No se pudo guardar"
    return render_template("registro.html")
   
@app.route("/recuperarcontraseña", methods=["GET", "POST"])
def recuperar_contraseña():
    return render_template('recuperarcontraseña.html')

@app.route("/perfiladmin", methods=["GET", "POST"])
def perfil_admin():
    return render_template("perfiladmin.html")

@app.route("/GestionPilotos", methods=["GET"])
def Gestion_pilotos():
    return render_template('GestionPilotos.html')

@app.route("/EditarPiloto", methods=["GET", "POST"])
def Editar_pilotos():
    return render_template('EditarPiloto.html')

@app.route("/GestionUsuarios", methods=["GET"])
def Gestion_Usuarios():
    return render_template('GestionUsuarios.html')

@app.route("/EditarUsuario", methods=["GET", "POST"])
def Editar_Usuarios():
    return render_template('EditarUsuario.html')

@app.route("/GestionVuelos", methods=["GET"])
def Gestion_Vuelos():
    return render_template('GestionVuelos.html')

@app.route("/CrearVuelos", methods=["GET", "POST"])
def Crear_Vuelos():
    return render_template('CrearVuelos.html')

@app.route("/EditarVuelos", methods=["GET", "POST"])
def Editar_Vuelos():
    return render_template('EditarVuelos.html')

@app.route("/GestionComentarios", methods=["GET"])
def Gestion_Comentarios():
    return render_template('GestionComentarios.html')

@app.route("/perfilpiloto", methods=["GET", "POST"])
def perfil_piloto():
    return render_template('perfilpiloto.html')

@app.route("/historialvuelospiloto", methods=["GET"])
def historial_vuelospiloto():
    return render_template('historialvuelospiloto.html')

@app.route("/perfilusuario", methods=["GET", "POST"])
def perfil_usuario():
    return render_template('perfilusuario.html')

@app.route("/itinerario", methods=["GET", "POST"])
def itinerario_usuario():
    return render_template('itinerariousuario.html')

@app.route("/reservausuario", methods=["GET", "POST"])
def reserva_usuario():
    return render_template('reservausuario.html')

@app.route("/comentariosusuario", methods=["GET", "POST"])
def comentarios_usuario():
    return render_template('comentariosusuario.html')

@app.route("/calificacionvuelosusuario", methods=["GET", "POST"])
def calificacionvuelos_usuario():
    return render_template('calificacionvuelosusuario.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)