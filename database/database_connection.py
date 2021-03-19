import psycopg2
import psycopg2.extras
import database.config as c
import alpaca_trade_api

# cursor info referenced: https://pynative.com/python-cursor-fetchall-fetchmany-fetchone-to-read-rows-from-table/
# PostgreSQL info referenced: https://realpython.com/python-sql-libraries/#postgresql
# Alpaca info
URL = c.ALPACA_URL
API_KEY_ID = c.API_KEY_ID
SECRET_KEY = c.SECRET_KEY

# database info
host = c.DB_HOST
name = c.DB_NAME
user = c.DB_USER
password = c.DB_PASSWORD


# connection to the database
def create_connection(host, name, user, password):
    try:
        connection = psycopg2.connect(
            host=host,
            database=name,
            user=user,
            password=password)
        print('Connection to PostgreSQL database successful.')
    except OperationalError as e:
        print(f'Error connecting to database; {e}')
    return connection


conn = create_connection(host, name, user, password)

# cursor is used to execute queries
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# alpaca trade api used to fetch stock information
api = alpaca_trade_api.REST(API_KEY_ID, SECRET_KEY, base_url=URL)