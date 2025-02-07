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

run_reading_list() {
    streamlit run .streamlit/streamlit_app.py
}

activate_venv
install_and_init
which python3
run_reading_list