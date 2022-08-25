import sqlite3
from sqlite3 import Error

def connect_database():
    try:
        db = sqlite3.connect('mydatabase.db')
        return db
    except Error:
        print(Error)
    # finally:
        # db.close()
        
def create_table(db):
    cursor_obj = db.cursor()
    cursor_obj.execute('CREATE TABLE servers(id text PRIMARY KEY, prefix text, admin_roles text)')
    db.commit()

def insert_server(db, objects):
    cursor_obj = db.cursor()
    cursor_obj.execute('INSERT INTO servers(id, prefix, admin_roles) VALUES(?, ?, ?)', objects)
    db.commit()

def query(db, server_id, col):
    cursor_obj = db.cursor()
    cursor_obj.execute('SELECT {} FROM servers WHERE id = {}'.format(col, server_id))
    return cursor_obj.fetchone()

def update_record(db, server_id, col, to):
    cursor_obj = db.cursor()
    cursor_obj.execute('UPDATE servers SET {} = {} WHERE id = {}'.format(col, to, server_id))
    db.commit()
    