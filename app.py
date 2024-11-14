from models import Book
from db import create_books_table, get_duckdb
import duckdb

get_duckdb()
create_books_table()

# x = Book(title='Great Spanish Stories', author='Penguin', year=2014, category='Language')
# y = Book(title='The Mushroom at the End of the World', author='Anna Lowenhaupt Tsing', year=2015, category='Nature')

# query_db(f"SELECT 1 as id, '{x.title}' as title, '{x.author}' as author, '{x.year}' as year, '{x.category}' as category")

print(duckdb.sql("SELECT * FROM books"))

# x.insert_to_db()

# query_db("SELECT * FROM books")

# print(x)