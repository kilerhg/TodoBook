from flask import Flask, render_template, redirect, url_for, request, session
from authlib.integrations.flask_client import OAuth
import requests
import os

import funcoes
import dao


app = Flask(__name__)
app.secrect_key = '123'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    session['email'] = user_info['email']
    # do something with the token and profile
    return redirect('/')

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


@app.route("/biblioteca/<int:unique>")
def add_book_library(isbn):
    print(isbn)
    return render_template('library.html')



# @app.route("/cadastrar", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
        
#         username = request.form['user']
#         email = request.form['email']
#         password = request.form['password']
#         db, cursor = dao.connect_db()
#         dao.insert_user(db=db, cursor=cursor, username=username, email=email, pwd=password)
#     return render_template('register.html')


# @app.route("/entrar", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form['email']
#         password = request.form['password']
#         db, cursor = dao.connect_db()
#         _id = dao.get_id_by_email(cursor=cursor, email=email)
#         print(_id)
#     return render_template('login.html')


# @app.route("/logout")
# def log_out():
#     return "Aba logout"


if __name__ == "__main__":
    app.run(debug=True)

