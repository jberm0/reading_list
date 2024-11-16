import streamlit as st

books = st.Page("books.py", title="Books", icon="📖")
reading_list = st.Page("reading_list.py", title="Reading List", icon="📚")
finished_list = st.Page("finished_list.py", title="Finished", icon="✅")

pg = st.navigation([books, reading_list, finished_list])
pg.run()