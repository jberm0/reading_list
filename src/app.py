# from db import create_books_table, get_duckdb
from classes import Book, Table, ReadingList
from utils import get_arguments_input
import duckdb

# get_duckdb()
# create_books_table()


def create_book():
    args = get_arguments_input(["title", "author", "category"])

    print(args)

    new_book = Book(
        title=args.__getattribute__("title"),
        author=args.__getattribute__("author"),
        category=args.__getattribute__("category"),
    )

    new_book.validate_new_book()

    new_book.insert_to_local_table()

    print(new_book)


def view_table(table: Table):
    print(duckdb.execute(table.duckdb_query).pl())
    


if __name__ == "__main__":
    view_table(Table('data', 'reading_list', ReadingList.reading_list_schema))
