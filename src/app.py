from classes import Book, Table
from utils import get_arguments_input
import duckdb
from db import insert_to_local_table
from db import validate_new_entry


def create_book():
    args = get_arguments_input(["title", "author", "category"])

    print(args)

    new_book = Book(
        title=args.__getattribute__("title"),
        author=args.__getattribute__("author"),
        category=args.__getattribute__("category"),
    )

    validate_new_entry(
        path="./data/books.csv", book_id=new_book.book_id, title=new_book.title
    )

    insert_to_local_table(new_book, "books")

    print(new_book)


def view_table(table: Table):
    print(duckdb.execute(table.duckdb_query).pl())


if __name__ == "__main__":
    create_book()
    # view_table(Table('data', 'reading_list', ReadingList.reading_list_schema))
