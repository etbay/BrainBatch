# Based of code from https://www.geeksforgeeks.org/postgresql/postgresql-connecting-to-the-database-using-python/
import psycopg2
import argparse
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect(sql_func, sql_params: tuple):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        sql_func(conn, cur, sql_params)
       
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert_user(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, user_info: tuple[str, str]):
    cur.execute('SELECT * FROM Users WHERE Users.Username = %s;', (user_info[0],))
    
    if cur.fetchone() is None:
        cur.execute('INSERT INTO Users (Username, Password) VALUES (%s, %s)', (user_info[0], user_info[1]))
        conn.commit()
        print("Succesfully added new user.")
    else:
        print("Username already exists.")


def log_in_user(conn: psycopg2.extensions.connection, cur: psycopg2.extensions.cursor, user_info: tuple[str, str]):
    cur.execute('SELECT * FROM Users WHERE Users.Username = %s AND Users.Password = %s;', (user_info[0], user_info[1]))
    print("Incorrect username or password." if cur.fetchone() is None else "Correct username or password.")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", required=True, help="The name of the user.")
    arg_parser.add_argument("-p", required=True, help="The password of the user.")
    arg_parser.add_argument("-n", "--new_user", action="store_true", help="Whether or not this user is new.")
    args = arg_parser.parse_args()

    connect(insert_user if args.new_user else log_in_user, (args.u, args.p))
