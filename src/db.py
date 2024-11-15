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

def create_or_replace_table(schema, table, extension):
        duckdb.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
        duckdb.execute(
            f"""
            CREATE OR REPLACE TABLE {schema}.{table} 
            AS SELECT * FROM read_csv('./{schema}/{table}.{extension}')
            """
        )
        print(f"Updated table {schema}.{table} from path './{schema}/{table}.{extension}'")

def sync_table_to_local_file(schema, table, extension):
        table_name = f"{schema}.{table}"
        duckdb.execute(f"COPY {table_name} TO './{schema}/{table}.{extension}'")
        print(f"Copied {table_name} to './{schema}/{table}.{extension}'")