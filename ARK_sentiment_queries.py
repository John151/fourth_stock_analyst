from database import data_queries as q

# we are testing with just two dates right now
# more will be added and more interesting queries will become possible
# earlier date
date_1 = '2021-03-11'
# later date
date_2 = '2021-01-26'


"""this function calls query functions in 'date_queries' module, finds if any new stocks were added 
between the first and second date or removed between the second and first
to find newly added, date_1 should be most recent_date, date_2 a previous date
to find newly deleted, date_1 should be previous date, date_2 a more recent date
"""


def temporary_collection_of_functions(date_1, date_2):
    newly_changed_stocks_results = q.find_new_appearances(date_1, date_2)
    new_stock_id_list = q.list_changes_in_holdings(newly_changed_stocks_results)
    if bool(new_stock_id_list):
        new_stock_list = q.get_holding_change_stock_information(new_stock_id_list)
        return new_stock_list
        # new stock list example [[11841, 'DKNG', 'DraftKings Inc. Class A Common Stock', 'NASDAQ', False], [20366, 'BILL', 'Bill.com Holdings, Inc.', 'NYSE', False], [11841, 'DKNG', 'D
        # raftKings Inc. Class A Common Stock', 'NASDAQ', False], [20654, 'RBLX', 'Roblox Corporation', 'NYSE', False]]:


# temporary_collection_of_functions(date_1, date_2)
