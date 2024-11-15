import duckdb
import datetime as dt
import polars as pl


class Table:
    def __init__(self, schema, table):
        self.schema = schema
        self.table = table

        self.create_or_replace_table()

    @property
    def extension(self) -> str:
        return "csv"

    @property
    def local_path(self):
        return f"./{self.schema}/{self.table}.{self.extension}"

    @property
    def duckdb_table(self):
        return f"{self.schema}.{self.table}"

    @property
    def duckdb_query(self):
        query = f"SELECT * FROM {self.duckdb_table}"
        return query

    def create_or_replace_table(self):
        duckdb.execute(f"CREATE SCHEMA IF NOT EXISTS {self.schema};")
        duckdb.execute(
            f"""
            CREATE OR REPLACE TABLE {self.duckdb_table} 
            AS SELECT * FROM read_csv('./{self.schema}/{self.table}.csv')
            """
        )
        print("updated table from path")

    def sync_table_to_local_file(self):
        duckdb.execute(f"COPY data.books TO '{self.local_path}'")


class Book:
    def __init__(self, title, author, category):
        self.table = Table("data", "books")
        self.id = self.create_book_id()
        self.title = title
        self.author = author
        self.category = category
        self.added = dt.datetime.today()
        self.df = pl.DataFrame(
            {
                key: self.__dict__.get(key)
                for key in ["id", "title", "author", "category", "added"]
            }
        )

        self.validate_new_book()

        self.insert_to_local_table()

    def create_book_id(self):
        books_count = duckdb.sql(
            f"SELECT COUNT() FROM read_csv('{self.table.local_path}')"
        ).pl()[0, 0]
        return books_count + 1

    def insert_to_local_table(self):
        df = self.df
        print(df)
        duckdb.execute("""INSERT INTO data.books SELECT * FROM df""")
        self.table.sync_table_to_local_file()

    def validate_new_book(self):
        query = f"""
            SELECT COUNT(*) AS count, id, title, author FROM read_csv('{self.table.local_path}')
            WHERE id = '{self.id}' OR LEVENSHTEIN(title, '{self.title}') < 5
            GROUP BY id, title, author
            ORDER BY id
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

    def add_to_reading_list():
        pass

    def finish():
        pass


class BooksFinished:
    pass


class ReadingList:
    pass

    def remove_book():
        pass

    def display_list():
        pass
