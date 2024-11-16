import streamlit as st
import duckdb
import sys

sys.path.append("././")

from src.backend.classes import FinishedList

st.write("# Finished")

FinishedList()
st.dataframe(
    duckdb.execute(
        """
        SELECT finished_id as id, title, author, rating, finished
        FROM data.finished
        """
    ).pl()
)

# TODO:
# - remove book from finished list