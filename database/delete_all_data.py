import database.database_connection as dc

connection = dc.conn
cursor = dc.cursor

delete_etf = 'delete from etf_holding;'
detete_stock = 'delete from stock;'
delete_stock_price = 'delete from stock_price;'
delete_mentions = 'delete from mentions;'

# this order is necessary, database has foreign key enforcement


def delete_all_database_data():
    delete_one_table_data(delete_etf)
    delete_one_table_data(detete_stock)
    delete_one_table_data(delete_stock_price)
    delete_one_table_data(delete_mentions)

  
def delete_one_table_data(delete_table):
    try:
        cursor.execute(delete_table)
        connection.commit()
        print(f'Executed {delete_table}')
    except Exception as e:
        print(f'Query {delete_table} failed; ', e)
        cursor.rollback()
