import streamlit as st

books = st.Page("books.py", title="Books", icon="📖")
reading_list = st.Page("reading_list.py", title="Reading List", icon="📚")
finished_list = st.Page("finished_list.py", title="Finished", icon="✅")
about = st.Page("about.py", title="About", icon="ℹ️")

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': 'https://www.extremelycoolapp.com/help',
        # 'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
    )

pg = st.navigation([reading_list, books, finished_list, about])
pg.run()
