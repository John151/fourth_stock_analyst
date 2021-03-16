import database.database_connection as dc

connection = dc.conn
cursor = dc.cursor


# get stock information by name ALL
def get_stock_information_by_id(stock_id):
    query = "SELECT * FROM stock WHERE id = %s"
    cursor.execute(query, (stock_id,))
    row = cursor.fetchone()
    return row


# function that gets all the information from API for new ARK additions
def get_holding_change_stock_information(change_stock_list):
    results = []
    for stock in change_stock_list:
        stock_full_information = get_stock_information_by_id(stock)
        results.append(stock_full_information)
    return results


# this query finds if any new stocks were added between the first and second date
# or removed between the second and first
# to find newly added, date_1 should be most recent_date, date_2 a previous date
# to find newly deleted, date_1 should be previous date, date_2 a more recent date
# ARK
def find_new_appearances(date_1, date_2):
    if date_1 > date_2:
        print('New stocks added')
    elif date_2 > date_1:
        print('Stocks no longer held')

    new_stocks_added = """
    SELECT stock_id
    FROM etf_holding
    where date_time = %s
    and stock_id NOT IN 
    (SELECT distinct(stock_id) FROM etf_holding WHERE
    date_time = %s)"""
    cursor.execute(new_stocks_added, (date_1, date_2))
    results = cursor.fetchall()
    return results


# function that puts changes in holdings in a list ARK
def list_changes_in_holdings(stock_changes_results):
    change_stocks_list = []
    for result in stock_changes_results:
        change_stocks_list.append(result[0])
    return change_stocks_list

