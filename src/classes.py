import duckdb
import datetime as dt
import polars as pl
from typing import List
from src.db import create_or_replace_table, sync_table_to_local_file
from src.utils import create_id, get_arguments_input

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
    book_schema = pl. Schema({'book_id': pl.Int64, 'title': pl.String, 'author': pl.String, 'category': pl.String, 'added': pl.Datetime(time_unit='us', time_zone=None)})

    def __init__(self, title, author, category):
        
        self.table = Table("data", "books", Book.book_schema)
        # self.book_id = create_id("./data/books.csv")
        self.title = title
        self.author = author
        self.category = category
        self.added = dt.datetime.today()
        # self.df = pl.DataFrame(
        #     {
        #         key: self.__dict__.get(key)
        #         for key in ["book_id", "title", "author", "category", "added"]
        #     }
        # )

        # self.validate_new_book()

        # self.insert_to_local_table()

    @property
    def book_id(self):
        return create_id("./data/books.csv")

    @property
    def book_df(self):
        attrs_dict = {
                key: self.__dict__.get(key)
                for key in ["book_id", "title", "author", "category", "added"]
            }
        attrs_dict['book_id'] = self.book_id
        return pl.DataFrame(attrs_dict)

    def insert_to_local_table(self):
        df = self.book_df # noqa
        duckdb.execute("""INSERT INTO data.books SELECT * FROM df""")
        print(duckdb.sql("SELECT * FROM data.books"))
        sync_table_to_local_file(schema='data', table='books', extension='csv')

    def validate_new_book(self):
        query = f"""
            SELECT COUNT(*) AS count, book_id, title, author FROM read_csv('{self.table.local_path}')
            WHERE book_id = '{self.book_id}' OR LEVENSHTEIN(title, '{self.title}') < 5
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

    def delete_book(self, table):
        query = f"""
                DELETE FROM data.'{table}' WHERE book_id = '{self.book_id}'
                """
        duckdb.execute(query)
        print(f"Deleted from data.'{table}' where book_id is {self.book_id}")
        sync_table_to_local_file(schema='data', table=table, extension='csv')
        print(f"Synced to local filesystem")

    def add_to_reading_list(self):
        suggested_by = get_arguments_input(['suggested_by']).__getattribute__('suggested_by')
        ToRead(self.title, self.author, self.category, suggested_by)


class ToRead(Book):

    def __init__(self, title, author, category, suggested_by):
        super().__init__(title, category, author)
        self.suggested_by = suggested_by
        self.added = dt.datetime.today()
        self.list_id = create_id('./data/reading_list.csv')

        print(self.book_id)

        print(self.list_df)

    @property
    def book_id(self):
        return super().book_id

    @property
    def list_df(self):
        attrs_dict = {
                key: self.__dict__.get(key)
                for key in ["list_id", "title", "author", "suggested_by", "added"]
            }
        attrs_dict['book_id'] = self.book_id
        return pl.DataFrame(attrs_dict)


    def remove_from_reading_list():
        pass

    def finish():
        pass


class BooksFinished(List[Book]):
    pass


class ReadingList:
    reading_list_schema = pl. Schema({'book_id': pl.Int64, 'list_id': pl.Int64, 'title': pl.String, 'author': pl.String, 'suggested_by': pl.String, 'added': pl.Datetime(time_unit='us', time_zone=None)})
    
    def __init__(self) -> None:
        self.table = Table('data', 'reading_list', ReadingList.reading_list_schema)
