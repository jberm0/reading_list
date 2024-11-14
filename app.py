from models import Book
from db import query_db

x = Book(title='test', author='jonah', year=2024, category='fun')

print(x)

query_db("SELECT * FROM books")

x.insert_to_db()

print(x)