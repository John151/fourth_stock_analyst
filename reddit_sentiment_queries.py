import database.data_queries as queries


def find_number_mentions(date, end_date):
    print('Finding most mentioned stocks...')
    rows = queries.calculate_number_mentions_date(date, end_date)
    return rows
