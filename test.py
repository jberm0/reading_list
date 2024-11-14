# from models import Book
import os
import polars as pl

# print(read_local_json('books', 1))

# df = read_local_json('books', 1)
# duckdb.execute(f"SELECT * FROM df")

# # Book(title='The Mushroom at the End of the World', author='Anna Lowenhaupt Tsing', year=2015, category='Nature')

print(os.listdir("./data/books"))

print(
    pl.concat([pl.read_json(f"./data/books/{p}") for p in os.listdir("./data/books")])
)
