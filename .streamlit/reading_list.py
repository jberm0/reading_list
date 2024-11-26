import streamlit as st
import duckdb
import sys
import datetime as dt
import polars as pl

sys.path.append("././")

from src.classes import init_db, Finished
from src.db import delete_book, validate_new_entry, insert_to_local_table

init_db()

st.title("Reading List")

st.dataframe(
    duckdb.execute(
        """
        SELECT list_id as id, title, author, suggested_by, added
        FROM data.reading_list
        """
    ).pl()
)

st.sidebar.title("Finish Book")
with st.sidebar.form("Finish Book"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    rating = st.number_input("Rating out of 10", min_value=0, max_value=10, step=1, value=None)

    submitted = st.form_submit_button("Submit")

count_matches = duckdb.execute(
    f"""
        SELECT COUNT(*)
        FROM data.reading_list
        WHERE title = '{title}'
        AND author = '{author}'
        """
).pl()[0, 0]

if submitted:
    if count_matches > 0:
        st.write(
        f"""
        Book found in the reading list \n
        Adding to finished list
        """)

        category = duckdb.execute(
                f"""
                    SELECT category
                    FROM data.books
                    WHERE title = '{title}'
                    AND author = '{author}'
                    """
            ).pl()[0, 0]

        suggested_by = duckdb.execute(
                            f"""
                                SELECT suggested_by
                                FROM data.reading_list
                                WHERE title = '{title}'
                                AND author = '{author}'
                                """
                        ).pl()[0, 0]

        finished_book = Finished(title, author, category, suggested_by, rating)

        is_valid = validate_new_entry("finished", finished_book.book_id, finished_book.title)

        if is_valid:
            insert_to_local_table(finished_book, "finished")
            delete_book(finished_book, "reading_list")

    else:
        st.write("No match found in reading list for that title and author, please check inputs")



# TODO:
# - add functionality to finish a book on reading list
# - remove book from reading list
