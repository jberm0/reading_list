import polars as pl
import os


def write_input_to_local_json(df: pl.DataFrame, table: str, id: int):
    path = f"./data/{table}"
    if not os.path.exists(path):
        os.makedirs(path)
    return df.write_json(path + f"/{id}.json")


def read_local_json(table: str, id: int) -> pl.DataFrame:
    return pl.read_json(f"./data/{table}/{id}.json")
