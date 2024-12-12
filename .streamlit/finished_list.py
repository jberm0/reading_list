import streamlit as st
import duckdb
import sys

sys.path.append("././")

from src.classes import init_db
from src.db import sync_table_to_local_file

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
        query = f"DELETE FROM data.finished WHERE finished_id = '{id}' AND title = '{title}' AND author = '{author}'"
        duckdb.execute(query)
        print(f"Deleted from data.finished where finished_id is {id}, title is {title} and author is {author}")
        sync_table_to_local_file(schema="data", table="finished", extension="csv")
        print("Synced to local filesystem")
        st.write(f"Removed {title} by {author} from finished list")

    st.button("Clear")

finished_books()