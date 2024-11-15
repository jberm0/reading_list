import duckdb
import polars as pl
from typing import Optional


def get_duckdb() -> duckdb.duckdb.DuckDBPyConnection:
    return duckdb.connect("./database.db")


def query_db(query) -> Optional[pl.DataFrame]:
    with get_duckdb() as db:
        result = db.sql(query)

        try:
            return result.pl()
        except AttributeError:
            return None

    # books_df = pl.concat(  # noqa
    #     [pl.read_json(f"./data/books/{p}") for p in os.listdir("./data/books")]
    # )
    # duckdb.execute(
    #     """
    #     INSERT INTO books
    #     SELECT * FROM books_df
    #     """
    # )
