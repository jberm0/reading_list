#!/bin/bash

source .venv/bin/activate

echo "initialised virtual environment"

poetry install --no-root

echo "installed and updated required libraries"