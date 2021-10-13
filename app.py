from flask import Flask, render_template, request, flash, redirect, url_for
import utils
import yagmail
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("registro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registro", methods=["GET",'POST'])
def register():

        if request.method == "POST":
            pass1 = request.form["password"]
            email1 = request.form["correo"]
            error = None
            
            if pass1 == "123456" and email1 == "leonardperez1992@gmail.com":
                return render_template("perfilsuperadmi.html")
            else:
                error = "Email o contraseña inválida"
                flash(error)


    #         if not utils.ispasswordvalid(pass1):
    #             error = "Contraseña inválida"
    #             flash(error)
    #             return render_template("registro.html")

    #         if not utils.isemailvalid(email1):
    #             error = "Correo invalido"
    #             flash(error)
    #             return render_template("registro.html")
            
    #         yag = yagmail.SMTP('pruebamintic2022', 'minTic2022*')
    #         yag.send(to=email1, subject="Activa tu cuenta", contents="Bienvenido, usa este link para activar tu cuenta")
    #         flash("Revisa tu correo para activar tu cuenta")
    #         return render_template("login.html")
    #     return render_template("register.html")
    # except:
    #     return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)