import streamlit as st
import duckdb
import sys

sys.path.append("././")

from src.backend.classes import ReadingList

ReadingList()
st.dataframe(
    duckdb.execute(
        """
        SELECT *
        FROM data.reading_list
        """
    ).pl()
)
