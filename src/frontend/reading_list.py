import streamlit as st
import duckdb
import sys
import datetime as dt
import polars as pl

sys.path.append("././")

from src.backend.classes import ReadingList

st.write("# Reading List")

ReadingList()
st.dataframe(
    duckdb.execute(
        """
        SELECT list_id as id, title, author, suggested_by, added
        FROM data.reading_list
        """
    ).pl()
)

# with st.sidebar("# Finish Book"):
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

        st.dataframe(duckdb.execute(
            f"""
                SELECT book_id, title, author, '{rating}' as rating, '{dt.datetime.today()}' as finished
                FROM data.reading_list
                WHERE title = '{title}'
                """
        ).pl())
    else:
        st.write("No match found in reading list for that title and author, please check inputs")



# TODO:
# - add functionality to finish a book on reading list
# - remove book from reading list
