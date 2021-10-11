from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("Login.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)