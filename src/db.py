import duckdb
import polars as pl
from typing import Optional
import os

def get_duckdb() -> duckdb.duckdb.DuckDBPyConnection:
    return duckdb.connect("./database.db")

def query_db(query) -> Optional[pl.DataFrame]:
    with get_duckdb() as db:
        result = db.sql(query)

        try:
            return result.pl()
        except AttributeError:
            return None

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def check_or_create_path(path):
    if not os.path.exists(path):
        touch(path)
    assert os.path.exists(path)

def check_path_exists(path):
    return os.path.exists(path)

def create_or_replace_table(schema, table, extension, pl_schema):
        duckdb.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
        file_path = f'./{schema}/{table}.{extension}'
        if os.path.exists(file_path):
            duckdb.execute(
                f"""
                CREATE OR REPLACE TABLE {schema}.{table} 
                AS SELECT * FROM read_csv('./{schema}/{table}.{extension}')
                """
            )
            print(f"Updated table {schema}.{table} from path './{schema}/{table}.{extension}'")
        else:
            touch(file_path)
            print(f"created file at path {file_path}")
            df = pl.DataFrame(schema=pl_schema)
            print(df)
            df.write_csv(file_path, include_header=True)
        

def sync_table_to_local_file(schema, table, extension):
        table_name = f"{schema}.{table}"
        duckdb.execute(f"COPY {table_name} TO './{schema}/{table}.{extension}'")
        print(f"Copied {table_name} to './{schema}/{table}.{extension}'")

def display_db_table(schema, table):
    print(duckdb.execute(
        f"""
        SELECT * FROM '{schema}'.'{table}'
        """
    ).pl())

def display_fp_table(schema, table, extension):
    print(duckdb.execute(
        f"""
        SELECT * FROM read_'{extension}'('./{schema}/{table}/{extension}')
        """
    ).pl())