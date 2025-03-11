#!/bin/bash

echo "activating virtual environment"

activate_venv() {
    echo "Activating virtual environment: .venv"
    source ".venv/bin/activate"
}

install_and_init() {
    echo "Installing module and dependencies"
    poetry install --no-root
}

check_data_files() {
    local dir="./data"

    # check if data directory exists
    if [ ! -d "$dir" ]; then
        echo "Directory does not exist. Creating directory..."
        mkdir -p "$dir"
    fi

    # check if required tables exist, if not create with column headers
    if [ ! -f "$dir/books.csv" ]; then
        echo "File '$dir/books.csv' does not exist. Creating file and adding text..."
        echo "book_id,title,author,category,added" > "$dir/books.csv"
    else
        echo "$dir/books.csv exists"
    fi

    if [ ! -f "$dir/finished.csv" ]; then
        echo "File '$dir/finished.csv' does not exist. Creating file and adding text..."
        echo "book_id,finished_id,title,author,suggested_by,rating,finished" > "$dir/finished.csv"
    else
        echo "$dir/finished.csv exists"
    fi

    if [ ! -f "$dir/reading_list.csv" ]; then
        echo "File '$dir/reading_list.csv' does not exist. Creating file and adding text..."
        echo "book_id,list_id,title,author,suggested_by,added" > "$dir/reading_list.csv"
    else
        echo "$dir/reading_list.csv exists"
    fi
}

run_reading_list() {
    streamlit run .streamlit/streamlit_app.py
}

activate_venv
install_and_init
which python3
check_data_files
run_reading_list