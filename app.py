from flask import Flask, render_template, redirect, url_for, request, session
from authlib.integrations.flask_client import OAuth
from datetime import timedelta
import os
import secrets

import funcoes
import dao
import parameters

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
    is_logged = bool(dict(session))
    print(is_logged)
    return render_template('index.html', is_logged=is_logged)


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
    is_logged = bool(dict(session))
    lista_livros = []
    if request.method == "POST":
        livro = request.form["book_name"]
        lista_livros = funcoes.search_book(busca=livro)
    return render_template('search.html', books=lista_livros, is_logged=is_logged)


@app.route("/biblioteca")
@login_required
def library():
    db, cursor = dao.connection_database(user=parameters.USER, password=parameters.PWD, host=parameters.HOSTNAME, port=parameters.PORT, database=parameters.DATABASE)
    id_user = dict(session)['profile']['id']
    list_books_id = dao.get_id_books_by_user_id(cursor=cursor, id_user=id_user, schema=parameters.SCHEMA)
    dict_other_infos_book = dao.get_books_by_user_id(cursor=cursor, id_user=id_user, schema=parameters.SCHEMA)
    list_books = funcoes.get_books_by_id(list_books_id=list_books_id)
    new_list_books = []
    for x in list_books:
        x['id_status_book'] = dict_other_infos_book[x['book_id']]['id_status_book']
        x['percent_book'] = dict_other_infos_book[x['book_id']]['percent_book']
        new_list_books.append(x)
    dict_books = {pos:book for pos, book in enumerate(new_list_books)}
    return render_template(
        'library.html',
        user_session=dict(session)['profile'],
        dict_books=dict_books,
        )


@app.route("/biblioteca/add/<book_id>")
@login_required
def add_book_library(book_id):
    db, cursor = dao.connection_database(user=parameters.USER, password=parameters.PWD, host=parameters.HOSTNAME, port=parameters.PORT, database=parameters.DATABASE)

    id_user = dict(session)['profile']['id']

    book_exist = dao.get_id_register(cursor=cursor, id_user=id_user, google_book_id=book_id, schema=parameters.SCHEMA)
    
    if not book_exist:
        dao.insert_book_into_library_by_id(db=db, cursor=cursor, id_user=id_user, google_book_id=book_id), schema=parameters.SCHEMA
    return redirect('/biblioteca')

@app.route("/biblioteca/update", methods=['POST'])
@login_required
def update_book_library():
    id_user = dict(session)['profile']['id']

    status = request.form["status"]
    book_id = request.form["book_id"]
    percent = request.form['percent']

    if percent == '':
        percent = 0


    if int(status) in [0, 1, 2]:
        status = int(status)
    else:
        status = 0
    
    if int(percent) in list(range(101)) and int(status) not in [0, 2]:
        percent = int(percent)
    elif int(status) == 2:
        percent = 100
    else:
        percent = 0



    db, cursor = dao.connection_database(user=parameters.USER, password=parameters.PWD, host=parameters.HOSTNAME, port=parameters.PORT, database=parameters.DATABASE)
    id_register = dao.get_id_register(cursor=cursor, id_user=id_user, google_book_id=book_id, schema=parameters.SCHEMA)
    dao.update_status_book_by_id(cursor, db, new_status_book=status, id_register=id_register, schema=parameters.SCHEMA)
    dao.update_percent_book_by_id(cursor, db, new_percent=percent, id_register=id_register, schema=parameters.SCHEMA)

    return redirect('/biblioteca')


@app.route("/biblioteca/remove/<book_id>")
@login_required
def remove_book_library(book_id):
    db, cursor = dao.connection_database(user=parameters.USER, password=parameters.PWD, host=parameters.HOSTNAME, port=parameters.PORT, database=parameters.DATABASE)

    id_user = dict(session)['profile']['id']
    dao.remove_book_from_library_by_id(db=db, cursor=cursor, id_user=id_user, google_book_id=book_id, schema=parameters.SCHEMA)
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

