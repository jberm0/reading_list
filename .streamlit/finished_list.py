import streamlit as st
import duckdb
import sys

sys.path.append("././")

from src.classes import init_db
from src.db import delete_finished_book

def finished_books():

    st.title("Finished Books")

    init_db()

    st.dataframe(
        duckdb.execute(
            """
            SELECT finished_id as id, title, author, suggested_by, rating, finished
            FROM data.finished
            """
        ).pl()
    )

    st.sidebar.title("Remove Book")
    with st.sidebar.form("Remove Book"):
        id = st.number_input("ID", value=None)
        title = st.text_input("Title", value=None)
        author = st.text_input("Author", value=None)

        submitted = st.form_submit_button("Submit")

    if submitted:
        delete_finished_book(id=id, title=title, author=author)
        st.write(f"Removed {title} by {author} from finished list")

    st.button("Clear")

finished_books()