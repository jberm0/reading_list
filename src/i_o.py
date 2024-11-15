import polars as pl
from typing import Dict


def write_input_to_local_json(content: Dict, table: str, id: int):
    path = f"./data/{table}.csv"
    # if not os.path.exists(path):
    #     os.makedirs(path)
    with open(path, "a") as f:
        f.write(str(content))
    # return df.write_json(path + f"/{id}.json")


def read_local_json(table: str, id: int) -> pl.DataFrame:
    return pl.read_json(f"./data/{table}/{id}.json")
