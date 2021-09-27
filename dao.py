import os
import psycopg2
import parameters
import logging

def connection_database(user, password, host, port, database):
    try:
        db = psycopg2.connect(user=user,
                                        password=password,
                                        host=host,
                                        port=port,
                                        database=database)
        cursor = db.cursor()
        logging.info('Successful connection')
        return db, cursor
    except:
        logging.CRITICAL('Connection error')

def insert_book_into_library_by_id(db, cursor, id_user, google_book_id, schema):
    sql_query_insert_book_into_library = f'''
            insert into book_library(id_user, book_unique_key, id_status_book, percent_book) values 
            ('{id_user}', '{google_book_id}', '0', '0');'''
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(sql_query_insert_book_into_library)
    db.commit()


def remove_book_from_library_by_id(db, cursor, id_user, google_book_id, schema):
    id_register = get_id_register(cursor=cursor, id_user=id_user, google_book_id=google_book_id, schema=schema)
    sql_query_remove_book_into_library = f'''
    delete from book_library
    where id_register='{id_register}'
    '''
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(sql_query_remove_book_into_library)
    db.commit()


def get_id_register(cursor, id_user, google_book_id, schema):
    sql_query_get_id_register = f'''
            select id_register from book_library
            where id_user = '{id_user}'
            and book_unique_key = '{google_book_id}';'''
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(sql_query_get_id_register)
    register_id = cursor.fetchone()
    if register_id:
        register_id = register_id[0]
    else:
        register_id = None
    return register_id


def update_status_book_by_id(cursor, db, new_status_book, id_register, schema):
    sql_query_update_status_book = f'''
            update book_library
            set id_status_book = {new_status_book}
            where id_register={id_register}'''
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(sql_query_update_status_book)
    db.commit()


def update_percent_book_by_id(cursor, db, new_percent, id_register, schema):
    sql_query_update_percent_book = f'''
            update book_library
            set percent_book = {new_percent}
            where id_register = {id_register};'''
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(sql_query_update_percent_book)
    db.commit()

def get_id_books_by_user_id(cursor, id_user, schema):
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(f'''
        select book_unique_key from book_library
        where id_user = '{id_user}'
    ;'''
    )
    valores = cursor.fetchall()
    if valores:
        valores = [book[0] for book in valores]
    else:
        valores = []
    return valores

def get_books_by_user_id(cursor, id_user, schema):
    cursor.execute(f"set schema '{schema}'")
    cursor.execute(f'''
        select book_unique_key, id_status_book, percent_book from book_library
        where id_user = '{id_user}'
    ;'''
    )
    valores = cursor.fetchall()
    if valores:
        valores = {book[0]:{'id_status_book':book[1], 'percent_book':book[2]} for book in valores}
    else:
        valores = {}
    return valores