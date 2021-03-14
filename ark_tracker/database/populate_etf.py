"""
Tracking ARK Invest ETFs with Python and PostgreSQL
Part Time Larry
https://www.youtube.com/watch?v=5uW0TLHQg9w
"""

import csv
import database_connection as dc

connection = dc.conn
cursor = dc.cursor

cursor.execute("SELECT * FROM stock WHERE is_etf = TRUE")

etfs = cursor.fetchall()

# hard code for now, make adjustable
file_date = '2021-01-26'
# TODO when automating the csv file download, remove the last 3 lines

# loops through ETFs, finds stock in portfolio, checks if stock exists in stocks database
# if it does, pull information and add to etf_holdings database
for etf in etfs:
    print(etf['symbol'])
    with open(f"../data/{file_date}/{etf['symbol']}.csv") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            ticker = row[3]
            if ticker:
                date = row[0]
                shares = row[5]
                weight = row[7]
                cursor.execute("""
                SELECT * FROM stock WHERE symbol = %s
                """, (ticker,))
                stock = cursor.fetchone()
                if stock:
                    cursor.execute("""
                    INSERT INTO etf_holding (etf_id, stock_id, date_time, shares, weight)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (etf['id'], stock['id'], date, shares, weight))

connection.commit()
connection.close()