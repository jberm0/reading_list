import duckdb


def create_id(file_path, column):
    current_count = duckdb.sql(f"SELECT MAX({column})+1 FROM read_csv('{file_path}')").pl()[
        0, 0
    ]
    return current_count + 1
