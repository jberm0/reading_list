import streamlit as st
import sys
sys.path.append("././")

from src.backend.classes import Book



def create_book():
    with st.form("input book"):
        title = st.text_input("title")
        author = st.text_input("author")
        category = st.text_input("category")

        submitted = st.form_submit_button("Submit")

    if submitted:
        new_book = Book(
            title=title,
            author=author,
            category=category,
        )

        st.write(new_book)

create_book()