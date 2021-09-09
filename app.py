from flask import Flask, render_template, redirect, url_for, request
import requests

import funcoes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/busca", methods=["GET", "POST"])
def search():
    lista_livros = []
    if request.method == "POST":
        livro = request.form["book_name"]
        lista_livros = funcoes.search_book(busca=livro)
    return render_template('search.html', books=lista_livros)

@app.route("/biblioteca")
def library():
    return render_template('library.html')

@app.route("/biblioteca/<int:isbn>")
def add_book_library(isbn):
    print(isbn)
    return render_template('library.html')

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

