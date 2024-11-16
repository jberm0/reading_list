import duckdb


def create_id(file_path):
    current_count = duckdb.sql(f"SELECT COUNT() FROM read_csv('{file_path}')").pl()[
        0, 0
    ]
    return current_count + 1
