import duckdb
import datetime as dt
import polars as pl
from typing import List
from db import create_or_replace_table, sync_table_to_local_file
from utils import create_id

class Table:
    def __init__(self, schema, table, pl_schema):
        self.schema = schema
        self.table = table
        self.pl_schema = pl_schema

        create_or_replace_table(schema=self.schema, table=self.table, extension=self.extension, pl_schema=pl_schema)

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


class Book:
    book_schema = pl. Schema({'id': pl.Int64, 'title': pl.String, 'author': pl.String, 'category': pl.String, 'added': pl.Datetime(time_unit='us', time_zone=None)})

    def __init__(self, title, author, category):
        
        self.table = Table("data", "books", Book.book_schema)
        self.id = create_id("./data/books.csv")
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

    def insert_to_local_table(self):
        df = self.df # noqa
        duckdb.execute("""INSERT INTO data.books SELECT * FROM df""")
        print(duckdb.sql("SELECT * FROM data.books"))
        sync_table_to_local_file(schema='data', table='books', extension='csv')

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

    def delete_book():
        pass

    def remove_from_reading_list():
        pass

    def finish():
        pass


class BooksFinished(List[Book]):
    pass


class ReadingList:
    reading_list_schema = pl. Schema({'id': pl.Int64, 'title': pl.String, 'author': pl.String, 'suggested_by': pl.String, 'added': pl.Datetime(time_unit='us', time_zone=None)})
    
    def __init__(self) -> None:
        self.table = Table('data', 'reading_list', ReadingList.reading_list_schema)

    def add_book(self, Book):
        pass

    def finish_book(self, Book):
        pass

    def display_list(self):
        print(duckdb.execute(
            f"""
            SELECT * FROM data.reading_list
            """
        ).pl())
