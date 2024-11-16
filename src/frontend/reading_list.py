import streamlit as st
import duckdb
import sys

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

# TODO:
# - add functionality to finish a book on reading list
# - remove book from reading list
