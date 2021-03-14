import database_connection as dc

connection = dc.conn
cursor = dc.cursor

# we are testing with just two dates right now
# more will be added and more interesting queries will become possible
# earlier date
date_2 = '2021-03-11'
# later date
date_1 = '2021-01-26'


# this query finds if any new stocks were added between the first and second date
# or removed between the second and first
# to find newly added, date_1 should be most recent_date, date_2 a previous date
# to find newly deleted, date_1 should be previous date, date_2 a more recent date

def find_new_appearances(date_1, date_2):
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


# function that puts changes in holdings in a list
def list_changes_in_holdings(stock_changes_results):
    change_stocks_list = []
    for result in stock_changes_results:
        change_stocks_list.append(result[0])
    return change_stocks_list


# function that gets all the information from API for new ARK additions
def get_holding_change_stock_information(change_stock_list):
    get_stock_information_by_id = "SELECT * FROM stock WHERE id = %s"
    results = []
    for stock in change_stock_list:
        cursor.execute(get_stock_information_by_id, (stock,))
        row = cursor.fetchone()
        results.append(row)
    return results

def temporary_collection_of_functions():
    newly_changed_stocks_results = find_new_appearances(date_1, date_2)
    new_stock_id_list = list_changes_in_holdings(newly_changed_stocks_results)
    if bool(new_stock_id_list):
        new_stock_list = get_holding_change_stock_information(new_stock_id_list)
        print(new_stock_list)
        # new stock list example [[11841, 'DKNG', 'DraftKings Inc. Class A Common Stock', 'NASDAQ', False], [20366, 'BILL', 'Bill.com Holdings, Inc.', 'NYSE', False], [11841, 'DKNG', 'D
        # raftKings Inc. Class A Common Stock', 'NASDAQ', False], [20654, 'RBLX', 'Roblox Corporation', 'NYSE', False]]:


temporary_collection_of_functions()

connection.close()
