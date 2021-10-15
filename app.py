from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("registro.html")

@app.route("/registro", methods=['GET', 'POST'])
def login():
    try:
        if request.method == "POST":
            user1 = request.form["correo"]
            pass1 = request.form["password"]
            error = None
            print("Estoy aquí")
            
            if (user1 == "leonardperez1992@gmail.com" and pass1 == "Persona123"):
                render_template("perfilsuperadmi.html")
            else:
                error = "Usuario o contraseña inválidos"
                flash(error)
                return render_template("perfilsuperadmi.html")
        else:
            return render_template("Login.html")
    except:
        return render_template("Login.html")



if __name__ == '__main__':
    app.run(debug=True, port=8000)