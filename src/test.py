from classes import Book, Table, ReadingList
from db import validate_new_entry, insert_to_local_table
import duckdb
import polars as pl
import datetime as dt

# print(read_local_json('books', 1))

# df = read_local_json('books', 1)
# print(duckdb.execute(f"SELECT * FROM read_csv('./data/books.csv')").pl())

# x = Book(title='deleting a book', author='jonah', category='testing')

# validate_new_entry('./data/books.csv', x.book_id, x.title)

# insert_to_local_table(x, 'books')

# x.add_to_reading_list()

# print(duckdb.execute(f"SELECT * FROM data.books").pl())

# x.delete_book()

# print(duckdb.execute(f"SELECT * FROM data.books").pl())

# reading_list = Table("data", "reading_list")
# print(books.duckdb_query)

# print(duckdb.sql(books.duckdb_query).pl())

# ts = pl.date(dt.datetime.today())
# print(type(ts))

x = ReadingList()

print(duckdb.execute(
        f"""
        SELECT * FROM data.reading_list
        """
    ).pl())

# print(type(pl.read_csv('./data/books.csv').schema))