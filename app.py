from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def inicio():
    return render_template("Login.html")

@app.route("/", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user1 = request.form['correo']
            pass1 = request.form['password']
            error = None
            if not user1:
                error = "Usuario Vacío"
                flash(error)
                return render_template("Login.html")
            if not pass1:
                error = "Contraseña Vacío"
                flash(error)
                return render_template("Login.html")
            if (user1 == "Persona@gmail.com" and pass1 == "Persona123"):
                return redirect("perfiladmin")
            if (user1 == "Persona2@gmail.com" and pass1 == "Persona123"):
                return redirect("perfilpiloto")
            if (user1 == "Persona3@gmail.com" and pass1 == "Persona123"):
                return redirect("perfilusuario")
            else:
                error = "Usuario o contraseña inválidos"
                flash(error)
                return render_template("Login.html")
        else:
            return render_template("Login.html")
    except:
        return render_template("Login.html")


@app.route("/registro")
def registro():
    return render_template("registro.html", methods=["GET", "POST"])

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