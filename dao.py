import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

def connect_db(name='database'):

    if os.path.isfile(f'./{name}.db'):
        db = sqlite3.connect(f"{name}.db")
        cursor = db.cursor()
    else:
        db = sqlite3.connect(f"{name}.db")
        cursor = db.cursor()

        sql_query_generate_users = '''
            CREATE TABLE users (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username TEXT(50) NOT NULL,
                email TEXT(50) NOT NULL UNIQUE,
                password TEXT(200) NOT NULL
            );'''

        sql_query_generate_status_book = '''
            CREATE TABLE status_book (
                id_status INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                description TEXT(50)
            );'''

        sql_query_generate_library = '''
            CREATE TABLE library (
                id_register INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                id_user INTEGER NOT NULL,
                book_unique_key TEXT(40),
                id_status_book INTEGER,
                percent_book FLOAT(3),
                FOREIGN KEY(id_user) REFERENCES users(id)
                FOREIGN KEY(id_status_book) REFERENCES status_book(id_status)
            );'''

        sql_query_insert_status_book = '''
            insert into status_book(id_status, description) values 
            ('0', 'Not Stated'), 
            ('1', 'Reading'),
            ('2', 'Readed');'''

        cursor.execute(sql_query_generate_users)
        cursor.execute(sql_query_generate_status_book)
        cursor.execute(sql_query_generate_library)

        cursor.execute(sql_query_insert_status_book)
        db.commit()

        
    
    return db, cursor

def insert_user(db, cursor, username : str, email : str, pwd : str):
    hash_password = generate_password_hash(pwd)
    query_insert = f"""
    insert into users(username, email, password) 
    values ('{username}', '{email}', '{hash_password}');"""
    try:
        cursor.execute(query_insert)
    except sqlite3.IntegrityError:
        return 'E-mail ja cadastrado'

    db.commit()

def login_user(cursor, email, pwd):
    query_login = f'''
    select password from users where email = '{email}';
    '''
    
    cursor.execute(query_login)


    hash_password = cursor.fetchone()

    if hash_password:
        if check_password_hash(hash_password[0], pwd):
            return True
        else:
            return 'senha incorreta'
    else:
        return 'email não existente'

def get_id_by_email(cursor, email : str):
    query = f'''
        select (id) from users
        where email = '{email}';
    '''
    cursor.execute(query)
    value = cursor.fetchone()

    if value:
        value = value[0]
    else:
        value = None

    return value
        

def update_password_by_id(cursor, db, id_user, password : str):
    query = f'''
    UPDATE users
    set password = '{password}'
    where id = '{id_user}'
    '''
    cursor.execute(query)
    db.commit()

def update_email_by_id(cursor, db, id_user, email : str):
    query = f'''
    UPDATE users
    set email = '{email}'
    where id = '{id_user}'
    '''
    cursor.execute(query)
    db.commit()

def update_username_by_id(cursor, db, id_user, username : str):
    query = f'''
    UPDATE users
    set username = '{username}'
    where id = '{id_user}'
    '''
    cursor.execute(query)
    db.commit()