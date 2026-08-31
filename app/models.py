from contextlib import contextmanager
import sqlite3

@contextmanager
def db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    try:
        yield conn, cur
    finally:
        conn.close()