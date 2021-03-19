import database.database_connection as dc
import psycopg2

connection = dc.conn
cursor = dc.cursor


# get stock information by name ALL
def get_stock_information_by_id(stock_id):
    query = "SELECT * FROM stock WHERE id = %s"
    cursor.execute(query, (stock_id,))
    row = cursor.fetchone()
    return row


# get list of all stocks from stock table ALL
def get_all_stock_information():
    query = 'SELECT * FROM stock'
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


# add new mentions on subreddits to the mentions table
def add_new_mentions(dt, id, message, source, url, mention_type):
    query = """INSERT INTO mentions
                (date_time, stock_id, message, source, url, mention_type)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
    try:
        cursor.execute(query, (dt, id, message, source, url, mention_type))
        connection.commit()
    except Exception as e:
        print('Error adding new mention; ', e)
        connection.rollback()


# finds number of mentions of a stock by date
# reddit
def calculate_number_mentions_date(date, end_date):
    query = """SELECT count(*) as number_mentions, stock_id, symbol, name
               FROM mentions JOIN stock on stock.id = mentions.stock_id
               WHERE date_time BETWEEN %s and %s
               GROUP BY stock_id, symbol, name
               ORDER BY number_mentions;"""
    cursor.execute(query, (date, end_date))
    rows = cursor.fetchall()
    return rows

# processes information already in database, counts number of mentions for all data available during last week
# reddit
def calculate_number_mentions_last_week():
    query = """SELECT count(*) as number_mentions, stock_id, symbol, name
               FROM mentions JOIN stock on stock.id = mentions.stock_id
               WHERE date_time > now() - interval '1 week'
               GROUP BY stock_id, symbol, name
               ORDER BY number_mentions;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


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
    try:
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
    except psycopg2.InterfaceError as e:
        print(e)
        connection.rollback()


# function that puts changes in holdings in a list ARK
def list_changes_in_holdings(stock_changes_results):
    change_stocks_list = []
    for result in stock_changes_results:
        change_stocks_list.append(result[0])
    return change_stocks_list


# finds largest holdings by percentage at most recent date ARK
def list_largest_holdings(limit):
    largest_holdings = """SELECT weight, symbol, name
                          FROM etf_holding JOIN stock on stock.id = etf_holding.stock_id
                          WHERE date_time = (SELECT MAX(date_time) FROM etf_holding)
                          ORDER BY weight DESC
                          LIMIT %s"""
    cursor.execute(largest_holdings, (limit,))
    results = cursor.fetchall()
    return results

# TODO fix function, should return largest holding for each fund
# def largest_holdings_by_fund(date):
#     largest_holdings_by_fund = """SELECT DISTINCT ON (etf_id)
#                                   etf_id, max(weight) as weight, name
#                                   FROM etf_holding JOIN stock on stock.id = etf_holding.stock_id
#                                   GROUP by etf_id, name"""
#     cursor.execute(largest_holdings_by_fund, (date,))
#     results = cursor.fetchall()
#     return results

