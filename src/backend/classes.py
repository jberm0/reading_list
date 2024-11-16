import datetime as dt
import polars as pl
import duckdb
import streamlit as st
import sys
sys.path.append("././")

from src.backend.db import (
    create_or_replace_table,
    validate_new_entry,
    insert_to_local_table,
    delete_book
)
from src.backend.utils import create_id, get_arguments_input


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

    # def add_to_reading_list(self):
    #     suggested_by = st.text_input("Who suggested this book?")
    #     book_to_read = ToRead(self.title, self.author, self.category, suggested_by)
    #     ReadingList()  # noqa
    #     validate_new_entry(
    #         "./data/reading_list.csv", book_to_read.book_id, book_to_read.title
    #     )
    #     insert_to_local_table(book_to_read, "reading_list")
    #     return book_to_read

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
        dict = {"book_id": self.book_id}
        dict.update(attrs_dict)
        return pl.DataFrame(dict)

    # def finish(self):
    #     rating = get_arguments_input(["rating"]).__getattribute__("rating")
    #     FinishedList()
    #     print(duckdb.execute("SHOW ALL TABLES").pl())
    #     finished_book = Finished(self.title, self.author, self.category, self.suggested_by, rating)
    #     validate_new_entry(
    #         "./data/finished.csv", finished_book.book_id, finished_book.title
    #     )
    #     insert_to_local_table(finished_book, "finished")

class Finished(ToRead):
    def __init__(self, title, author, category, suggested_by, rating):
        super().__init__(title, author, category, suggested_by)
        self.finished = dt.datetime.today()
        self.finished_id = create_id("./data/finished.csv")
        self.rating = rating

        delete_book(self, 'reading_list')

    @property
    def book_id(self):
        return super().book_id

    @property
    def finished_df(self):
        attrs_dict = {
            key: self.__dict__.get(key)
            for key in ["finished_id", "title", "author", "rating", "finished"]
        }
        attrs_dict["book_id"] = self.book_id
        return pl.DataFrame(attrs_dict)


class FinishedList:
    finished_list_schema = pl.Schema(
        {
            "book_id": pl.Int64,
            "finished_id": pl.Int64,
            "title": pl.String,
            "author": pl.String,
            "rating": pl.String,
            "finished": pl.Datetime(time_unit="us", time_zone=None),
        }
    )

    def __init__(self) -> None:
        self.table = Table("data", "finished", FinishedList.finished_list_schema)


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
