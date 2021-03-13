import psycopg2
import config as c
from database_connection import connection


connection = psycopg2.connect(host=c.DB_HOST, database=c.DB_NAME, user=c.DB_USER, password=c.DB_PASSWORD)
