import database.database_connection as dc
import database.data_queries as queries
import reddit_tracker.scrape as scrape

connection = dc.conn
cursor = dc.cursor


def insert_mentions(title_list, comment_list):
    title_count = 1
    comment_count = 1

    for title_entry in title_list:
        print(f'adding title entry {title_count}')
        title_count = title_count + 1
        queries.add_new_mentions(title_entry['date_time'], title_entry['id'], title_entry['body'],
                                 title_entry['subreddit'], title_entry['url'], title_entry['submission_type'])
    for comment_entry in comment_list:
        print(f'adding comment entry {comment_count}')
        comment_count = comment_count + 1
        queries.add_new_mentions(comment_entry['date_time'], comment_entry['id'], comment_entry['body'],
                                 comment_entry['subreddit'], comment_entry['url'], comment_entry['submission_type'])


# gets list of possible stock symbols from reddit comments for given date
def scrape_comment_mentions_by_date(stocks, year, month, day, max):
    print('Scraping comment data...')
    comment_cache = scrape.scrape_wsb_comments_by_date(year, month, day, max)
    comment_list = scrape.parse_comment_data(comment_cache, stocks)
    print('Returning comment list.')
    return comment_list


# gets list of possible stock symbols from reddit post titles for given date
def scrape_title_mentions_by_date(stocks, year, month, day):
    print('Scraping data by date...')
    title_cache = scrape.scrape_wsb_by_date(year, month, day)
    title_list = scrape.parse_submission_data(title_cache, stocks)
    print('Returning list.')
    return title_list


# creates dictionary, key is stock symbol, value is stock id
def make_stock_dictionary():
    print('Creating stock dictionary $$$')
    rows = queries.get_all_stock_information()
    stocks = {}
    for row in rows:
        stocks['$' + row['symbol']] = row['id']
    return stocks


def populate(year, month, day, max):
    stocks = make_stock_dictionary()
    title_list = scrape_title_mentions_by_date(stocks, year, month, day)
    comment_list = scrape_comment_mentions_by_date(stocks, year, month, day, max)
    insert_mentions(title_list, comment_list)



# populate(2021, 3, 16, 5000)

