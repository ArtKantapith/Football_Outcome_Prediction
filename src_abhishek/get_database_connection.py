import sqlite3

def get_connection_object(database = '../data/database.sqlite'):

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn