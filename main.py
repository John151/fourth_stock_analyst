from reddit_tracker import scrape
import reddit_sentiment_queries as reddit
from datetime import datetime
import database.create_tables as create
import ARK_sentiment_queries as ark
import database.populate_mentions as pop_mentions
import database.populate_etf as pop_etf

now = datetime.now().strftime("%Y-%m-%d")
date = '2021-3-16'
date_end_search = '2021-3-17'
file_date = '2021-03-18'
second_newest_file_date = '2021-03-11'


def main():
    print('Beginning process...')
    pop_mentions.populate(2021, 3, 16, 2000)
    reddit_mentions = reddit.find_number_mentions(date, date_end_search)
    print(f'Most mentioned stocks on /r/wallstreetbets on {date}')
    for row in reddit_mentions:
        print(row)

    pop_etf.populate_etf_data(file_date)
    newly_added = ark.ark_change_information(file_date, second_newest_file_date)
    print('Newly added to the ARK holdings:')
    for new_addition in newly_added:
        print(new_addition)
    newly_removed = ark.ark_change_information(second_newest_file_date, file_date)
    print('Recently removed from ARK holdings:')
    for new_subtraction in newly_removed:
        print(new_subtraction)
    largest_holdings = ark.ark_largest_holdings_current(10)
    print('The largest holdings currently in ARK etfs:')
    for holding in largest_holdings:
        print(holding)




# create all tables
#create.create_all_tables()

# delete all tables
#delete_all_database_data()

# ark information
#pop_etf.populate_etf_data(file_date)
#newly_added = ark.ark_change_information(date_1, date_2)
#newly_removed = ark.ark_change_information(date_2, date_1)
#largest_holdings = ark_largest_holdings_current(limit)

# reddit info
#pop_mentions.populate(year, month, day, max)
#reddit.find_number_mentions(date=now)
#calculate_number_mentions_last_week()
#calculate_number_mentions_date(date)

if __name__ == "__main__":
    main()

