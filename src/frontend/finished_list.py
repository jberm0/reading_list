import streamlit as st
import duckdb
import sys
sys.path.append("././")

from src.backend.classes import FinishedList

FinishedList()
st.dataframe(duckdb.execute("""
        SELECT *
        FROM data.finished
        """).pl())