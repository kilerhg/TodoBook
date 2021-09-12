import sqlite3
import os

def connect_db(name='database'):

    if os.path.isfile(f'./{name}.db'):
        db = sqlite3.connect(f"{name}.db")
        cursor = db.cursor()
    else:
        db = sqlite3.connect(f"{name}.db")
        cursor = db.cursor()

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
                FOREIGN KEY(id_status_book) REFERENCES status_book(id_status)
            );'''

        sql_query_insert_status_book = '''
            insert into status_book(id_status, description) values 
            ('0', 'Not Stated'), 
            ('1', 'Reading'),
            ('2', 'Readed');'''

        cursor.execute(sql_query_generate_status_book)
        cursor.execute(sql_query_generate_library)

        cursor.execute(sql_query_insert_status_book)
        db.commit()
    
    return db, cursor


def insert_book_into_library_by_id(db, cursor, id_user, google_book_id):
    sql_query_insert_book_into_library = f'''
            insert into library(id_user, book_unique_key, id_status_book, percent_book) values 
            ('{id_user}', '{google_book_id}', '0', '0');'''
    cursor.execute(sql_query_insert_book_into_library)
    db.commit()


def remove_book_from_library_by_id(db, cursor, id_user, google_book_id):
    id_register = get_id_register(cursor=cursor, id_user=id_user, google_book_id=google_book_id)
    sql_query_remove_book_into_library = f'''
    delete from library
    where id_register='{id_register}'
    '''
    cursor.execute(sql_query_remove_book_into_library)
    db.commit()


def get_id_register(cursor, id_user, google_book_id):
    sql_query_get_id_register = f'''
            select id_register from library
            where id_user = '{id_user}'
            and book_unique_key = '{google_book_id}';'''
    cursor.execute(sql_query_get_id_register)
    register_id = cursor.fetchone()
    if register_id:
        register_id = register_id[0]
    else:
        register_id = None
    return register_id


def update_status_book_by_id(cursor, db, new_status_book, id_register):
    sql_query_update_status_book = f'''
            update library
            set id_status_book = {new_status_book}
            where id_register={id_register}'''
    cursor.execute(sql_query_update_status_book)
    db.commit()


def update_percent_book_by_id(cursor, db, new_percent, id_register):
    sql_query_update_percent_book = f'''
            update library
            set percent_book = {new_percent}
            where id_register = {id_register};'''
    cursor.execute(sql_query_update_percent_book)
    db.commit()

def get_id_books_by_user_id(cursor, id_user):
    cursor.execute(f'''
        select book_unique_key from library
        where id_user = '{id_user}'
    ;'''
    )
    valores = cursor.fetchall()
    if valores:
        valores = [book[0] for book in valores]
    else:
        valores = []
    return valores