from flask import Flask, render_template, redirect, url_for, request, session
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os
import secrets

import funcoes
import dao

import logging

from auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

secret = secrets.token_urlsafe(32)

app = Flask(__name__)
# app.secrect_key = secret
# app.secrect_key = os.getenv("APP_SECRET_KEY")
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")


app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

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
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session['user'] = user
    # session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route("/busca", methods=["GET", "POST"])
def search():
    lista_livros = []
    if request.method == "POST":
        livro = request.form["book_name"]
        lista_livros = funcoes.search_book(busca=livro)
        print(lista_livros)
    return render_template('search.html', books=lista_livros)


@app.route("/biblioteca")
@login_required
def library():
    db, cursor = dao.connect_db()
    id_user = dict(session)['profile']['id']
    list_books_id = dao.get_id_books_by_user_id(cursor=cursor, id_user=id_user)
    list_books = funcoes.get_books_by_id(list_books_id=list_books_id)
    return render_template(
        'library.html',
        user_session=dict(session)['profile'],
        list_books=list_books,
        )

@app.route("/biblioteca/add/<book_id>")
@login_required
def add_book_library(book_id):
    db, cursor = dao.connect_db()

    id_user = dict(session)['profile']['id']

    book_exist = dao.get_id_register(cursor=cursor, id_user=id_user, google_book_id=book_id)
    
    if not book_exist:
        dao.insert_book_into_library_by_id(db=db, cursor=cursor, id_user=id_user, google_book_id=book_id)
    return redirect('/biblioteca')

@app.route("/biblioteca/remove/<book_id>")
@login_required
def remove_book_library(book_id):
    db, cursor = dao.connect_db()

    id_user = dict(session)['profile']['id']
    dao.remove_book_from_library_by_id(db=db, cursor=cursor, id_user=id_user, google_book_id=book_id)
    return redirect('/biblioteca')


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

