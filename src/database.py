
def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: None
    """

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id SERIAL PRIMARY KEY,
                                        user_name TEXT NOT NULL,
                                        user_email TEXT NOT NULL
                                    ); """

    sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                    post_id SERIAL PRIMARY KEY,
                                    post_title TEXT NOT NULL,
                                    post_content TEXT NOT NULL,
                                    post_author TEXT NOT NULL,
                                    post_date TEXT NOT NULL
                                );"""


    try:
        c = conn.cursor()
        c.execute(sql_create_posts_table)
        c.execute(sql_create_users_table)
    except Exception as e:
        print(e)
    finally:
        conn.commit()

def create_user(conn, name="Anon", email="sample@web.com"):
    """
    Create a new user into the users table
    :param conn: Connection object
    :param user: tuple with user info
    :return: project id
    """
    sql = ''' INSERT INTO users(user_name,user_email)
              VALUES(%s,%s) RETURNING user_id'''
    
    user = (name, email)
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.fetchone()

def create_post(conn, post):
    sql = """
        INSERT INTO posts(post_title, post_content, post_author, post_date)
        VALUES(%s,%s,%s,%s)
    """
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.fetchone()

def delete_user(conn, email):
    """
    Delete a task by user by id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM users WHERE user_email=%s'
    cur = conn.cursor()
    cur.execute(sql, (email,))
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
            SELECT * FROM posts WHERE post_title=%s AND post_date=%s
    """

    cur = conn.cursor()
    cur.execute(sql, (title,date))
    data = cur.fetchone()
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
    cur.execute("SELECT * FROM users WHERE user_email=%s", (email,))
    data = cur.fetchone()
    return True if data else False

def get_users(conn):
    """
    Database query for all registered users
    """

    cur = conn.cursor()
    cur.execute("SELECT user_email FROM users")
    data = cur.fetchall()
    return [email[0] for email in data]
