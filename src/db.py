import duckdb
import polars as pl
import os


def create_or_replace_table(schema, table, extension, pl_schema):
    duckdb.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    file_path = f"./{schema}/{table}.{extension}"
    if os.path.exists(file_path):
        duckdb.execute(
            f"""
                CREATE OR REPLACE TABLE {schema}.{table} 
                AS SELECT * FROM read_csv('./{schema}/{table}.{extension}')
                """
        )
        print(
            f"Updated table {schema}.{table} from path './{schema}/{table}.{extension}'"
        )
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
    print(
        duckdb.execute(
            f"""
        SELECT * FROM '{schema}'.'{table}'
        """
        ).pl()
    )


def validate_new_entry(path: str, book_id: int, title: str):
    query = f"""
        SELECT COUNT(*) AS count, book_id, title, author FROM read_csv('{path}')
        WHERE book_id = '{book_id}' OR LEVENSHTEIN(title, '{title}') < 5
        GROUP BY book_id, title, author
        ORDER BY book_id
    """
    matches_query = duckdb.sql(query).pl()
    duplicate_message = f"""
            The book you are trying to enter may already exist in the table, please check the table of matches:
            {matches_query}
            """
    if not matches_query.is_empty():
        assert matches_query[0, 0] == 0, duplicate_message
    else:
        return True


def insert_to_local_table(book, table):
    if table == "reading_list":
        schema, table, extension = "data", "reading_list", "csv"
        df = book.list_df  # noqa

    elif table == "books":
        schema, table, extension = "data", "books", "csv"
        df = book.book_df  # noqa
    duckdb.execute(f"""INSERT INTO {schema}.{table} SELECT * FROM df""")
    print(duckdb.sql(f"SELECT * FROM {schema}.{table}"))
    sync_table_to_local_file(schema=schema, table=table, extension=extension)


def touch(path):
    with open(path, "a"):
        os.utime(path, None)


def check_or_create_path(path):
    if not os.path.exists(path):
        touch(path)
    assert os.path.exists(path)


def check_path_exists(path):
    return os.path.exists(path)


def display_fp_table(schema, table, extension):
    print(
        duckdb.execute(
            f"""
        SELECT * FROM read_'{extension}'('./{schema}/{table}/{extension}')
        """
        ).pl()
    )

def delete_book(book, table):
    query = f"""
            DELETE FROM data.'{table}' WHERE book_id = '{book.book_id}'
            """
    duckdb.execute(query)
    print(f"Deleted from data.'{table}' where book_id is {book.book_id}")
    sync_table_to_local_file(schema="data", table=table, extension="csv")
    print("Synced to local filesystem")