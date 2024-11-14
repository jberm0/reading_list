import duckdb
import os
import polars as pl

def get_duckdb() -> duckdb.duckdb.DuckDBPyConnection:
    return duckdb.connect('./database.db')

def create_books_table():
    duckdb.execute(
        """
        CREATE OR REPLACE TABLE books (
            id integer primary key NOT NULL,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(50),
            year INT,
            category VARCHAR(20)
            )
        """
    )
    books_df = pl.concat([pl.read_json(f'./data/books/{p}') for p in os.listdir('./data/books')])
    duckdb.execute(
        """
        INSERT INTO books
        SELECT * FROM books_df
        """
    )