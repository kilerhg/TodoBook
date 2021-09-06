from flask import Flask, render_template, redirect, url_for

import funcoes



app = Flask(__name__)


@app.route("/")
def index():
    return render_template('home_page.html')

@app.route("/busca")
def search():
    return render_template('search.html')

@app.route("/cadastrar")
def register():
    return "Aba cadastrar"

@app.route("/login")
def login():
    return "Aba login"

@app.route("/logout")
def log_out():
    return "Aba logout"


if __name__ == "__main__":
    app.run(debug=True)

