import streamlit as st
import sys
sys.path.append("././")

from src.backend.classes import Book, ToRead, ReadingList
from src.backend.db import validate_new_entry, insert_to_local_table


def create_book():
    with st.form("add book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        category = st.text_input("Category")
        add_to_reading_list = st.checkbox("Add this book to reading list?")
        suggested_by = st.text_input("Who suggested this book?")

        submitted = st.form_submit_button("Submit")

    if submitted:
        new_book = Book(
            title=title,
            author=author,
            category=category,
        )

        if not add_to_reading_list:
            is_valid_book = validate_new_entry(
                table="books", book_id=new_book.book_id, title=new_book.title
            )

            if is_valid_book:
                insert_to_local_table(new_book, "books")
                st.write(f"{new_book.title} added to books database")
                st.dataframe(new_book.book_df)

            if not is_valid_book:
                st.write("You can add this book to the reading list by submitting the form again, but make sure you select option to add to reading list")

        if add_to_reading_list:
            is_valid_reading_list = validate_new_entry(
                    "reading_list", new_book.book_id, new_book.title
                )

            if is_valid_reading_list:
                book_to_read = ToRead(new_book.title, new_book.author, new_book.category, suggested_by)
                ReadingList()  # noqa
                insert_to_local_table(book_to_read, "reading_list")
                st.write(f"{book_to_read.title} added to reading list")
                st.dataframe(book_to_read.list_df)

            else:
                st.write("This may already exist in the reading list, try again.")
        
        st.button("Clear")

create_book()