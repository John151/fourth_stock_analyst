
CREATE TABLE IF NOT EXISTS stock (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    is_etf BOOLEAN NOT NULL
);

-- compound key etf_id + stock_id + date_time
CREATE TABLE IF NOT EXISTS etf_holding (
    etf_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    date_time DATE NOT NULL,
    shares NUMERIC,
    weight NUMERIC,
    PRIMARY KEY (etf_id, stock_id, date_time),
    CONSTRAINT fk_etf_id FOREIGN KEY (etf_id) REFERENCES stock (id),
    CONSTRAINT fk_stock_id FOREIGN KEY (stock_id) REFERENCES stock (id)
);

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
);

CREATE INDEX ON stock_price (stock_id, date_time DESC);

SELECT create_hypertable('stock_price', 'date_time'); 