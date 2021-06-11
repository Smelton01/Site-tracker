import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: None
    """

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text,
                                        email text NOT NULL
                                    ); """

    sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    content text NOT NULL,
                                    author text NOT NULL,
                                    date_added text NOT NULL
                                );"""


    try:
        c = conn.cursor()
        c.execute(sql_create_posts_table)
        c.execute(sql_create_users_table)
    except Error as e:
        print(e)

def create_user(conn, name="Anon", email="sample@web.com"):
    """
    Create a new user into the users table
    :param conn: Connection object
    :param user: tuple with user info
    :return: project id
    """
    sql = ''' INSERT INTO users(name,email)
              VALUES(?,?) '''
    
    user = (name, email)
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def create_post(conn, post):
    sql = """
        INSERT INTO posts(title, content, author, date_added)
        VALUES(?,?,?,?)
    """
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.lastrowid

def delete_user(conn, id):
    """
    Delete a task by user by id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def check_post(conn, title, date):
    """
    Check if a post has been seen before
    :param conn:  Connection to the SQLite database
    :param title: title of post :str
    :param date: date posted :date
    :return: boolean 
    """
    sql = """
            SELECT * FROM posts WHERE title=? AND date_added=?
    """

    cur = conn.cursor()
    cur.execute(sql, (title,date))
    data = cur.fetchall()
    return True if data else False
    
def check_user(conn, name, email):
    """
    Check if a user is registered in the database
    :param conn: Connection to the SQLite database
    :param name: User name
    :param email: User email address
    :returns: boolean
    """    
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    data = cur.fetchall()
    return True if data else False
