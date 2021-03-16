"""Module connects to our database, the alpaca API, gets a list of all tradable
stocks and commits them to the 'stock' table"""
from database.database_connection import api, cursor, conn

# fetches list stocks
assets = api.list_assets()

for asset in assets:
    if asset.tradable:
        print(f'Inserting stock {asset.name}, {asset.symbol}')
        cursor.execute("""
        INSERT INTO stock (symbol, name, exchange, is_etf)
        VALUES (%s, %s, %s, %s)
        """, (asset.symbol, asset.name, asset.exchange, False))

conn.commit()
conn.close()
