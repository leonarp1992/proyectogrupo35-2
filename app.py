from sqlite3.dbapi2 import Row
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import escape
import utils
import yagmail
import os
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
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
        correo = escape(request.form["correo"])
        password = escape(request.form["password"])
        tipoPerfiladmin = 1
        try:
            with sqlite3.connect('Plavue.db') as con: 
             cur = con.cursor()
             consulta = cur.execute("SELECT contraseña FROM Usuarios WHERE correo=? AND  tipoPerfil=?",[correo, tipoPerfiladmin]).fetchone()
             if consulta != None:
                 if check_password_hash(consulta[0], password):
                     session['usuario'] = correo
                     return redirect("/perfiladmin")
             elif request.method == "POST":
                 tipoPerfilpil = 2
                 try:
                     with sqlite3.connect('Plavue.db') as con: 
                         cur = con.cursor()
                         consulta = cur.execute("SELECT contraseña FROM Usuarios WHERE correo=? AND  tipoPerfil=?",[correo, tipoPerfilpil]).fetchone()
                         if consulta != None:
                             if check_password_hash(consulta[0], password):
                                 session['usuario'] = correo
                                 return redirect("/perfilpiloto")
                         elif request.method == "POST":
                             try:
                                 with sqlite3.connect('Plavue.db') as con: 
                                     cur = con.cursor()
                                     consulta = cur.execute("SELECT contraseña FROM Usuarios WHERE correo=?",[correo]).fetchone()
                                     if consulta != None:
                                         if check_password_hash(consulta[0], password):
                                             session['usuario'] = correo
                                             return redirect("/perfilusuario")
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
    if request.method == 'POST':
        nombre = request.form["Nombre"]
        correo = request.form["correo"]
        password =  generate_password_hash(request.form["password"])     
        try:
            with sqlite3.connect('Plavue.db') as con: #establecer objeto conexion a base de datos
                cur = con.cursor() #manipular la conexión a la bd
                cur.execute('INSERT INTO Usuarios (contraseña, Nombre, correo) VALUES (?,?,?)', (password, nombre,correo))
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
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con1:
                    con1.row_factory = sqlite3.Row
                    cur = con1.cursor()
                    cur.execute("SELECT * FROM tipo_documento")
                    query1 = cur.fetchall() 
                with sqlite3.connect("Plavue.db") as con2:
                    con2.row_factory = sqlite3.Row
                    cur = con2.cursor()
                    cur.execute("SELECT * FROM Perfil")
                    query2 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con3:
                    con3.row_factory = sqlite3.Row
                    cur = con3.cursor()
                    cur.execute("SELECT * FROM Estado")
                    query3 = cur.fetchall()
                with sqlite3.connect("Plavue.db") as con4:
                    con4.row_factory = sqlite3.Row
                    cur = con4.cursor()
                    cur.execute("SELECT * FROM Genero")
                    query4 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con5:
                    con5.row_factory = sqlite3.Row
                    cur = con5.cursor()
                    cur.execute("SELECT * FROM Nacionalidad")
                    query5 = cur.fetchall()                
                    if query is None:
                        return "Usuario no existe!"
                return render_template("perfiladmin.html", perfil = query, tipodocumento = query1, tipoperfil = query2, estado = query3, sexo = query4, pais = query5 )
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')  
        if request.method == "POST":
                documento = request.form["txtdocumento"]
                tipodocumento = request.form["listtipodocumento"]
                perfil = request.form["listperfil"]
                estado = request.form["listestado"]
                nombre = request.form["txtnombre"]
                fechanacimiento = request.form["txtfechanacimiento"]
                sexo = request.form["listsexo"]
                celular = request.form["txtcelular"]
                pais = request.form["listnacionalidad"]
                nombrecon = request.form["txtnombrecon"]
                celularcon = request.form["txtcelularcon"]
                # contraseña1 = request.form["txtcontraseña1"]
                # contraseña2 = request.form["txtcontraseña2"]
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=?, nombreContacto=?, numeroContacto=? WHERE correo=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, nombrecon, celularcon, session['usuario']))
                        con.commit()
                        return redirect('/perfiladmin')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("perfiladmin.html")   
    return render_template("Login.html")

@app.route("/GestionPilotos", methods=["GET"])
def Gestion_pilotos():
    if "usuario" in session:
        if request.method == "GET":
            tipoPerfil = "Piloto"
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con1:
                    con1.row_factory = sqlite3.Row
                    cur1 = con1.cursor()
                    cur1.execute("SELECT * FROM Usuarios WHERE tipoPerfil =? ", [tipoPerfil])
                    query2 = cur.fetchall()
                    if query2 is None:
                        return "Usuario no existe!"
                return render_template("GestionPilotos.html", perfil = query, tabla = query2)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
        return render_template('GestionPilotos.html')
    return render_template("Login.html")

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
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con1:
                    con1.row_factory = sqlite3.Row
                    cur = con1.cursor()
                    cur.execute("SELECT * FROM tipo_documento")
                    query1 = cur.fetchall() 
                with sqlite3.connect("Plavue.db") as con2:
                    con2.row_factory = sqlite3.Row
                    cur = con2.cursor()
                    cur.execute("SELECT * FROM Perfil")
                    query2 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con3:
                    con3.row_factory = sqlite3.Row
                    cur = con3.cursor()
                    cur.execute("SELECT * FROM Estado")
                    query3 = cur.fetchall()
                with sqlite3.connect("Plavue.db") as con4:
                    con4.row_factory = sqlite3.Row
                    cur = con4.cursor()
                    cur.execute("SELECT * FROM Genero")
                    query4 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con5:
                    con5.row_factory = sqlite3.Row
                    cur = con5.cursor()
                    cur.execute("SELECT * FROM Nacionalidad")
                    query5 = cur.fetchall()                
                    if query is None:
                        return "Usuario no existe!"
                return render_template("perfilpiloto.html", perfil = query, tipodocumento = query1, tipoperfil = query2, estado = query3, sexo = query4, pais = query5 )
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')  
        if request.method == "POST":
                documento = request.form["txtdocumento"]
                tipodocumento = request.form["listtipodocumento"]
                perfil = request.form["listperfil"]
                estado = request.form["listestado"]
                nombre = request.form["txtnombre"]
                fechanacimiento = request.form["txtfechanacimiento"]
                sexo = request.form["listsexo"]
                celular = request.form["txtcelular"]
                pais = request.form["listnacionalidad"]
                nombrecon = request.form["txtnombrecon"]
                celularcon = request.form["txtcelularcon"]
                # contraseña1 = request.form["txtcontraseña1"]
                # contraseña2 = request.form["txtcontraseña2"]
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=?, nombreContacto=?, numeroContacto=? WHERE correo=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, nombrecon, celularcon, session['usuario']))
                        con.commit()
                        return redirect('/perfilpiloto')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("perfilpiloto.html")   
    return render_template("Login.html")

@app.route("/historialvuelospiloto", methods=["GET"])
def historial_vuelospiloto():
    return render_template('historialvuelospiloto.html')

@app.route("/perfilusuario", methods=["GET", "POST"])
def perfil_usuario():
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con1:
                    con1.row_factory = sqlite3.Row
                    cur = con1.cursor()
                    cur.execute("SELECT * FROM tipo_documento")
                    query1 = cur.fetchall() 
                with sqlite3.connect("Plavue.db") as con2:
                    con2.row_factory = sqlite3.Row
                    cur = con2.cursor()
                    cur.execute("SELECT * FROM Perfil")
                    query2 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con3:
                    con3.row_factory = sqlite3.Row
                    cur = con3.cursor()
                    cur.execute("SELECT * FROM Estado")
                    query3 = cur.fetchall()
                with sqlite3.connect("Plavue.db") as con4:
                    con4.row_factory = sqlite3.Row
                    cur = con4.cursor()
                    cur.execute("SELECT * FROM Genero")
                    query4 = cur.fetchall()   
                with sqlite3.connect("Plavue.db") as con5:
                    con5.row_factory = sqlite3.Row
                    cur = con5.cursor()
                    cur.execute("SELECT * FROM Nacionalidad")
                    query5 = cur.fetchall()                
                    if query is None:
                        return "Usuario no existe!"
                return render_template("perfilusuario.html", perfil = query, tipodocumento = query1, tipoperfil = query2, estado = query3, sexo = query4, pais = query5 )
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')  
        if request.method == "POST":
                documento = request.form["txtdocumento"]
                tipodocumento = request.form["listtipodocumento"]
                perfil = request.form["listperfil"]
                estado = request.form["listestado"]
                nombre = request.form["txtnombre"]
                fechanacimiento = request.form["txtfechanacimiento"]
                sexo = request.form["listsexo"]
                celular = request.form["txtcelular"]
                pais = request.form["listnacionalidad"]
                nombrecon = request.form["txtnombrecon"]
                celularcon = request.form["txtcelularcon"]
                # contraseña1 = request.form["txtcontraseña1"]
                # contraseña2 = request.form["txtcontraseña2"]
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=?, nombreContacto=?, numeroContacto=? WHERE correo=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, nombrecon, celularcon, session['usuario']))
                        con.commit()
                        return redirect('/perfilusuario')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("perfilusuario.html")   
    return render_template("Login.html")

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