from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

#jsonify convierte un objeto a un json típico del navegador 
#from registroVuelos import vuelos

app = Flask(__name__)
    

@app.route('/')
def itinerario():
    try:
        with sqlite3.connect("itinerario.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM agendaVuelos")
            row = cur.fetchall()
            return render_template("itinerario-usuarioFinal.html", row = row)
    except Error:
        print(Error)

@app.route('/calificacion')
def calificacion():
    try:
        with sqlite3.connect("itinerario.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM agendaVuelos")
            rowcal = cur.fetchall()
            return render_template("calificacionVuelos-usuarioFinal.html", rowcal = rowcal)
    except Error:
        print(Error)

# @app.route('/calificacion')
# def calificacionEditar():
#     try:
#         with sqlite3.connect("itinerario.db") as con:
#             con.row_factory = sqlite3.Row
#             cur = con.cursor()
#             cur.execute("SELECT * FROM agendaVuelos")
#             rowcaledit = cur.fetchall()
#             return render_template("calificacionVuelos-usuarioFinal.html", rowcaledit = rowcaledit)
#     except Error:
#         print(Error)


@app.route('/comentarios')
def comentarios():
    return render_template("comentarios.html")

@app.route('/Comentarios/Busqueda', methods=['GET', 'POST'])
def busquedaComentarios():
    return

if __name__ == '__main__':
    app.run(debug=True, port=8000)