# from db import create_books_table, get_duckdb
from classes import Book
from utils import get_arguments_input

# get_duckdb()
# create_books_table()


def main():
    args = get_arguments_input(["title", "author", "category"])

    print(args)

    new_book = Book(
        title=args.__getattribute__("title"),
        author=args.__getattribute__("author"),
        category=args.__getattribute__("category"),
    )

    print(new_book)


if __name__ == "__main__":
    main()
