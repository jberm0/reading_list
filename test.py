from src.models import Table
import os
import polars as pl
import duckdb

# print(read_local_json('books', 1))

# df = read_local_json('books', 1)
# duckdb.execute(f"SELECT * FROM df")

# # Book(title='The Mushroom at the End of the World', author='Anna Lowenhaupt Tsing', year=2015, category='Nature')

books = Table('data', 'books')
print(books.duckdb_query)

print(duckdb.sql(books.duckdb_query).pl())