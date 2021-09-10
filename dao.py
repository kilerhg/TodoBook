import sqlite3

def connect_db(name='database'):
    db = sqlite3.connect(f"{name}.db")
    cursor = db.cursor()
    
    return db, cursor

db, cursor = connect_db()
