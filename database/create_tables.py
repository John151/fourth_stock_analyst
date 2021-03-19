import database.database_connection as dc

connection = dc.conn
cursor = dc.cursor


# runs 1 query, rolls back if fails
def create_table(query):
    try:
        cursor.execute(query)
        connection.commit()
        print(f'Executed {query}')
    except Exception as e:
        print(f'Query {query} failed; ', e)
        cursor.rollback()


# loops through each command for initial setup
def create_all_tables():
    every_sql_command = ['create_stock_table', 'create_etf_holding', 'create_stock_price'
                         'create_table_mentions', 'create_stock_price_index', 'create_stock_price_hypertable',
                         'create_mentions_index', 'create_mentions_hypertable']
    for command in every_sql_command:
        create_table(command)
    connection.close()

create_stock_table = '''
CREATE TABLE IF NOT EXISTS stock (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);'''

# compound key etf_id + stock_id + date_time
create_etf_holding = ''' 
CREATE TABLE IF NOT EXISTS etf_holding (
    etf_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    date_time DATE NOT NULL,
    shares NUMERIC,
    weight NUMERIC,
    PRIMARY KEY (etf_id, stock_id, date_time),
    CONSTRAINT fk_etf_id FOREIGN KEY (etf_id) REFERENCES stock (id),
    CONSTRAINT fk_stock_id FOREIGN KEY (stock_id) REFERENCES stock (id)
);'''

create_stock_price = '''
CREATE TABLE IF NOT EXISTS stock_price (
    stock_id INTEGER NOT NULL,
    date_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    PRIMARY KEY (stock_id, date_time),
    CONSTRAINT fk_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);'''

create_table_mentions = '''
CREATE TABLE IF NOT EXISTS mentions (
    stock_id INTEGER,
    date_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    message TEXT NOT NULL,
    source TEXT NOT NULL,
    mention_type TEXT NOT NULL,
    url TEXT NOT NULL,
    PRIMARY KEY (stock_id, date_time),
    CONSTRAINT fk_mention_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);'''

create_stock_price_index = 'CREATE INDEX ON stock_price (stock_id, date_time DESC);'
create_stock_price_hypertable = '''SELECT create_hypertable('stock_price', 'date_time');'''

create_mentions_index = 'CREATE INDEX ON mentions (stock_id, date_time DESC);'
create_mentions_hypertable = '''SELECT create_hypertable('mentions', 'date_time');'''
