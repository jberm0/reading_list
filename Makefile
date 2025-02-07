init:
	./src/init.sh

open:
	make init
	streamlit run ./.streamlit/streamlit_app.py

