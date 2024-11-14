from db import get_duckdb, query_db

class Book:
    
    def __init__(self, title, author, year, category):
        self.title = title
        self.author = author
        self.year = year
        self.category = category

    def insert_to_db(self):
        query_db(
            f"""INSERT INTO books (title, author, year, category) VALUES (
                {self.title}, {self.author}, {self.year}, {self.category}
            )"""
        )
        query_db("SELECT * FROM books")


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

