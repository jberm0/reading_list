# from db import create_books_table, get_duckdb
from models import Book

# get_duckdb()
# create_books_table()

x = Book(
    title="The Mushroom at the End of the World",
    author="Anna Lowenhaupt Tsing",
    category="Nature",
)
# y = Book(title='The Mushroom at the End of the World', author='Anna Lowenhaupt Tsing', category='Nature')

# query_db(f"SELECT 1 as id, '{x.title}' as title, '{x.author}' as author, '{x.year}' as year, '{x.category}' as category")

# print(duckdb.sql("SELECT * FROM books"))

# x.insert_to_db()

# query_db("SELECT * FROM books")

# print(x)

# x = Table("data", "books")

# x.create_or_replace_table()

# print(duckdb.execute("SELECT COUNT(*)+1 FROM data.books").pl()[0,0])
