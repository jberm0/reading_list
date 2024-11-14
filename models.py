import duckdb
from i_o import write_input_to_local_json, read_local_json
import os

class Book:

    def __init__(self, title, author, year, category):
        self.id = self.create_book_id()
        self.title = title
        self.author = author
        self.year = year
        self.category = category

        df = duckdb.sql(f"SELECT {self.id} as id, '{self.title}' as title, '{self.author}' as author, '{self.year}' as year, '{self.category}' as category").pl()

        write_input_to_local_json(df, 'books', self.id)

        self.insert_to_db()

    def create_book_id(self):
        return len(os.listdir('./data/books')) + 1

    def insert_to_db(self):
        df = read_local_json('books', self.id)
        duckdb.execute(f"INSERT INTO books SELECT * FROM df")

    def add_to_list():
        pass

    def finish():
        pass

class BooksFinished():
    pass


class ReadingList():
    pass

    def remove_book():
        pass

    def display_list():
        pass

