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
    if request.method == 'GET':
        with sqlite3.connect("Plavue.db") as con1:
            con1.row_factory = sqlite3.Row
            cur = con1.cursor()
            cur.execute("SELECT * FROM tipo_documento")
            query1 = cur.fetchall() 
            return render_template("registro.html", tipodocumento = query1)

    if request.method == 'POST':
        now = datetime.now()
        id_usuario = now.strftime("%Y%m%d%H%M%S")
        tipo_documento = request.form["listtipodocumento"]
        documento = request.form["txtdocumento"]
        nombre = request.form["Nombre"]
        correo = request.form["correo"]
        password1 = (request.form["password"])
        password2 = (request.form["confpassword"])
        tipoperfil = 3
        estado = 1
        if password1 == password2:
            password = generate_password_hash(password1)
            try:
                with sqlite3.connect('Plavue.db') as con: #establecer objeto conexion a base de datos
                    cur = con.cursor() #manipular la conexión a la bd
                    cur.execute('INSERT INTO Usuarios (Id_usuario, Documento, tipoDocumento, contraseña, Nombre, correo, tipoPerfil, estado) VALUES (?,?,?,?,?,?,?)', (id_usuario, documento, tipo_documento, password, nombre,correo, tipoperfil, estado))
                    con.commit() #confirmar la transacción
                    return render_template("Login.html")
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')
                return "No se pudo guardar"
        else:
            error = "Contraseña inválida"
            flash(error)
            return render_template("registro.html")
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
                # if contraseña1 == contraseña2:
                #     contraseña = generate_password_hash(contraseña1)
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?,Celular=?, nacionalidad=?, nombreContacto=?, numeroContacto=? WHERE correo=? ', (documento, tipodocumento, perfil, estado, nombre,fechanacimiento, sexo, celular, pais, nombrecon, celularcon, session['usuario']))
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
            tipoPerfil = 2
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
                    query2 = cur1.fetchall()
                    if query2 is None:
                        return "Usuario no existe!"
                return render_template("GestionPilotos.html", perfil = query, tabla = query2)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
        return render_template('GestionPilotos.html')
    return render_template("Login.html")

@app.route("/EditarPiloto", methods = ["GET", "POAT"])
@app.route("/EditarPiloto/<correo>", methods=["GET", "POST"])
def Editar_pilotos(correo):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con6:
                    con6.row_factory = sqlite3.Row
                    cur = con6.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [correo])
                    query6 = cur.fetchone()                    
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
                return render_template("EditarPiloto.html", perfil = query, tipodocumento = query1, tipoperfil = query2, estado = query3, sexo = query4, pais = query5, tabla = query6)
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
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=? WHERE documento=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, documento))
                        con.commit()
                        return redirect('/GestionPilotos')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("EditarPiloto.html")   
    return render_template("Login.html")

@app.route("/GestionUsuarios", methods=["GET"])
def Gestion_Usuarios():
    if "usuario" in session:
        if request.method == "GET":
            tipoPerfil = 3
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
                    query2 = cur1.fetchall()
                    if query2 is None:
                        return "Usuario no existe!"
                return render_template("GestionUsuarios.html", perfil = query, tabla = query2)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
        return render_template('GestionUsuarios.html')
    return render_template("Login.html")

@app.route("/EditarUsuario", methods=["GET", "POST"])
@app.route("/EditarUsuario/<correo>", methods=["GET", "POST"])
def Editar_Usuarios(correo):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con6:
                    con6.row_factory = sqlite3.Row
                    cur = con6.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [correo])
                    query6 = cur.fetchone()                    
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
                return render_template("EditarUsuario.html", perfil = query, tipodocumento = query1, tipoperfil = query2, estado = query3, sexo = query4, pais = query5, tabla = query6)
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
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=? WHERE documento=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, documento))
                        con.commit()
                        return redirect('/GestionUsuarios')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("EditarUsuarios.html")   
    return render_template("Login.html")

@app.route("/GestionVuelos", methods=["GET"])
def Gestion_Vuelos():
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
                    cur1 = con1.cursor()
                    cur1.execute("SELECT * FROM Vuelos")
                    query2 = cur1.fetchall()
                with sqlite3.connect("Plavue.db") as con2:
                    con2.row_factory = sqlite3.Row
                    cur2 = con2.cursor()
                    cur2.execute("SELECT * FROM Ciudades")
                    query3 = cur1.fetchall()
                    if query is None:
                        return "Usuario no existe!"
                return render_template("GestionVuelos.html", perfil = query, vuelos = query2, ciudad = query3)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
            return render_template("GestionVuelos.html")
    return render_template('Login.html')

@app.route("/CrearVuelos", methods=["GET", "POST"])
def Crear_Vuelos():
    if "usuario" in session:
        if request.method == "GET":
            tipoPerfil= 2
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con1:
                    con1.row_factory = sqlite3.Row
                    cur1 = con1.cursor()
                    cur1.execute("SELECT Nombre FROM Usuarios WHERE tipoPerfil =? ", [tipoPerfil])
                    query2 = cur1.fetchall()
                with sqlite3.connect("Plavue.db") as con2:
                    con2.row_factory = sqlite3.Row
                    cur2 = con2.cursor()
                    cur2.execute("SELECT * FROM Ciudades")
                    query3 = cur2.fetchall()
                    if query is None:
                        return "Usuario no existe!"
                return render_template("CrearVuelos.html", perfil = query, pilotos = query2, ciudades = query3 )
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
            return render_template("CrearVuelos.html")
        if request.method == "POST":
            now = datetime.now()
            id_vuelo = now.strftime("%Y%m%d%H%M%S")
            placa = request.form["txtplaca"]
            aereolinea = request.form["txtaereolinea"]
            ciud_origen = request.form["ciudorigen"]
            ciud_destino = request.form["ciudest"]
            hora_salida = request.form["hora-salida"]
            hora_llegada = request.form["hora-llegada"]
            fecha = request.form["fecha-salida"]
            estado = request.form["estadoVuelo"]
            capacidad = request.form["txtcappasajeros"]
            cupos = request.form["txtcuposdisponibles"]
            precio = request.form["txtprecio"]
            piloto = request.form["piloto"]
            try:
                with sqlite3.connect('Plavue.db') as con: #establecer objeto conexion a base de datos
                    cur = con.cursor() #manipular la conexión a la bd
                    cur.execute('INSERT INTO Vuelos (Id_vuelo, placa, aereolinea, origen, destino, horaSalida, horaLlegada, fecha, estado, capacidad, cupos, precio, piloto) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', (id_vuelo, placa, aereolinea , ciud_origen, ciud_destino, hora_salida, hora_llegada, fecha, estado, capacidad, cupos, precio, piloto))
                    con.commit() #confirmar la transacción
                    return redirect('/GestionVuelos')
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')
                return "No se pudo guardar"
    return render_template("Login.html")

@app.route("/EditarVuelos", methods=["GET", "POST"])
@app.route("/EditarVuelos/<Id_vuelo>", methods=["GET", "POST"]) 
def Editar_Vuelos(Id_vuelo):
    if "usuario" in session:
        if request.method == "GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("Plavue.db") as con6:
                    con6.row_factory = sqlite3.Row
                    cur = con6.cursor()
                    cur.execute("SELECT * FROM Vuelos WHERE correo = ?", [Id_vuelo])
                    query6 = cur.fetchone()                    
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
                return render_template("EditarVuelos.html", perfil = query, estado = query3, tabla = query6)
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
                try:
                    with sqlite3.connect('Plavue.db') as con:  
                        cur = con.cursor() #manipular la conexión a la bd
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, tipoPerfil=?, estadoUsuario=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=? WHERE documento=? ', (documento, tipodocumento, perfil, estado, nombre, fechanacimiento, sexo, celular, pais, documento))
                        con.commit()
                        return redirect('/GestionUsuarios')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("EditarUsuarios.html")   
    return render_template("Login.html")

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
                    cur1 = con1.cursor()
                    cur1.execute("SELECT * FROM Vuelospiloto")
                    query1 = cur1.fetchall()
                return render_template("historialvuelospiloto.html", perfil = query, vuelos = query1)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ') 
        return render_template("historialvuelospiloto.html")
    return render_template("Login.html")

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
                        cur.execute('UPDATE Usuarios SET Documento=?, tipoDocumento=?, Nombre=?, fechaNacimiento=?, sexo=?, Celular=?, nacionalidad=?, nombreContacto=?, numeroContacto=? WHERE correo=? ', (documento, tipodocumento, nombre, fechanacimiento, sexo, celular, pais, nombrecon, celularcon, session['usuario']))
                        con.commit()
                        return redirect('/perfilusuario')
                except Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print('SQLite traceback: ') 
        return render_template("perfilusuario.html")   
    return render_template("Login.html")

@app.route("/itinerario", methods=["GET", "POST"])
def itinerario_usuario():
    if "usuario" in session:
        if request.method =="GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("itinerario.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM agendaVuelos")
                    row = cur.fetchall()
                    return render_template("itinerario-usuarioFinal.html", perfil = query, row = row)
            except Error:
                print(Error)
            return render_template('itinerariousuario.html')
    return render_template ("Login.html")

@app.route("/reservausuario", methods=["GET", "POST"])
def reserva_usuario():
    if "usuario" in session:
        if request.method =="GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                    return render_template("reservausuario.html",perfil = query)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')  
            return render_template('itinerariousuario.html')
    return render_template ("Login.html")

@app.route("/comentariosusuario", methods=["GET", "POST"])
def comentarios_usuario():
    return render_template('comentariosusuario.html')

@app.route("/calificacionvuelosusuario", methods=["GET", "POST"])
def calificacionvuelos_usuario():
    if "usuario" in session:
        if request.method =="GET":
            try:
                with sqlite3.connect("Plavue.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Usuarios WHERE correo = ?", [session["usuario"]])
                    query = cur.fetchone()
                with sqlite3.connect("itinerario.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM agendaVuelos")
                    rowcal = cur.fetchall()
                    return render_template("calificacionVuelos-usuarioFinal.html",perfil = query, rowcal = rowcal)
            except Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print('SQLite traceback: ')  
            return render_template('itinerariousuario.html')
    return render_template ("Login.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)