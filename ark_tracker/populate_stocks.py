"""Module connects to our database, the alpaca API, gets a list of all tradable
stocks and commits them to the 'stock' table"""
import config as c
import alpaca_trade_api
import psycopg2
import psycopg2.extras
from database_connection import connection

# connection to the database
# cursor is used to execute queries
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

#alpaca trade api used to fetch stock information
api = alpaca_trade_api.REST(c.API_KEY_ID, c.SECRET_KEY, base_url=c.URL)

# fetches list stocks
assets = api.list_assets()

for asset in assets:
    if asset.tradable:
        print(f'Inserting stock {asset.name}, {asset.symbol}')
        cursor.execute("""
        INSERT INTO stock (symbol, name, exchange, is_etf)
        VALUES (%s, %s, %s, %s)
        """, (asset.symbol, asset.name, asset.exchange, False))

connection.commit()