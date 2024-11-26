import streamlit as st
import duckdb
import sys

sys.path.append("././")

from src.classes import FinishedList

st.title("Finished Books")

FinishedList()
st.dataframe(
    duckdb.execute(
        """
        SELECT finished_id as id, title, author, suggested_by, rating, finished
        FROM data.finished
        """
    ).pl()
)

# TODO:
# - remove book from finished list