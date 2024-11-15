import duckdb
import datetime as dt
import polars as pl
from db import (
    create_or_replace_table,
    sync_table_to_local_file,
    validate_new_entry,
    insert_to_local_table,
)
from utils import create_id, get_arguments_input


class Table:
    def __init__(self, schema, table, pl_schema):
        self.schema = schema
        self.table = table
        self.pl_schema = pl_schema

        create_or_replace_table(
            schema=self.schema,
            table=self.table,
            extension=self.extension,
            pl_schema=pl_schema,
        )

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
    book_schema = pl.Schema(
        {
            "book_id": pl.Int64,
            "title": pl.String,
            "author": pl.String,
            "category": pl.String,
            "added": pl.Datetime(time_unit="us", time_zone=None),
        }
    )

    def __init__(self, title, author, category):
        self.table = Table("data", "books", Book.book_schema)
        self.title = title
        self.author = author
        self.category = category
        self.added = dt.datetime.today()

    @property
    def book_id(self):
        return create_id("./data/books.csv")

    @property
    def book_df(self):
        attrs_dict = {
            key: self.__dict__.get(key)
            for key in ["book_id", "title", "author", "category", "added"]
        }
        attrs_dict["book_id"] = self.book_id
        return pl.DataFrame(attrs_dict)

    def add_to_reading_list(self):
        suggested_by = get_arguments_input(["suggested_by"]).__getattribute__(
            "suggested_by"
        )
        book_to_read = ToRead(self.title, self.author, self.category, suggested_by)
        reading_list = ReadingList()  # noqa
        validate_new_entry(
            "./data/reading_list.csv", book_to_read.book_id, book_to_read.title
        )
        insert_to_local_table(book_to_read, "reading_list")


class ToRead(Book):
    def __init__(self, title, author, category, suggested_by):
        super().__init__(title, category, author)
        self.suggested_by = suggested_by
        self.added = dt.datetime.today()
        self.list_id = create_id("./data/reading_list.csv")

    @property
    def book_id(self):
        return super().book_id

    @property
    def list_df(self):
        attrs_dict = {
            key: self.__dict__.get(key)
            for key in ["list_id", "title", "author", "suggested_by", "added"]
        }
        attrs_dict["book_id"] = self.book_id
        return pl.DataFrame(attrs_dict)

    def remove_from_reading_list():
        pass

    def finish():
        pass


class Finish(ToRead):
    pass


class ReadingList:
    reading_list_schema = pl.Schema(
        {
            "book_id": pl.Int64,
            "list_id": pl.Int64,
            "title": pl.String,
            "author": pl.String,
            "suggested_by": pl.String,
            "added": pl.Datetime(time_unit="us", time_zone=None),
        }
    )

    def __init__(self) -> None:
        self.table = Table("data", "reading_list", ReadingList.reading_list_schema)
