import database_connection as dc

connection = dc.conn
cursor = dc.cursor

# get all stocks table information, we will compare out scraper
# results to these to find matches
cursor.execute("""
    SELECT * FROM stock
    """)

rows = cursor.fetchall()
for row in rows:
    print('loop')
    print(row)
# stocks = {}
# for row in rows:
#     stocks