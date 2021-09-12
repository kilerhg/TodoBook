from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
import requests

import funcoes
import dao


app = Flask(__name__)


login_manager = LoginManager(app)


@login_manager.user_loader
def current_user(user_id):
    return user_id


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/busca", methods=["GET", "POST"])
@login_required
def search():
    lista_livros = []
    if request.method == "POST":
        livro = request.form["book_name"]
        lista_livros = funcoes.search_book(busca=livro)
    return render_template('search.html', books=lista_livros)


@app.route("/biblioteca")
@login_required
def library():
    return render_template('library.html')


@app.route("/biblioteca/<int:unique>")
@login_required
def add_book_library(isbn):
    print(isbn)
    return render_template('library.html')


@app.route("/cadastrar", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        username = request.form['user']
        email = request.form['email']
        password = request.form['password']
        db, cursor = dao.connect_db()
        dao.insert_user(db=db, cursor=cursor, username=username, email=email, pwd=password)
    return render_template('register.html')


@app.route("/entrar", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        db, cursor = dao.connect_db()
        _id = dao.get_id_by_email(cursor=cursor, email=email)
        print(_id)
    return render_template('login.html')


@app.route("/logout")
@login_required
def log_out():
    return "Aba logout"


if __name__ == "__main__":
    app.run(debug=True)

