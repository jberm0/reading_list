from typing import List
import duckdb


class Args:
    def __repr__(self):
        return str(vars(self))


def get_arguments_input(argument_names: List[str]):
    args = Args()

    for arg_name in argument_names:
        arg_val = input(f">>> enter {arg_name}: ")
        setattr(args, arg_name, arg_val)

    return args


def create_id(file_path):
    current_count = duckdb.sql(f"SELECT COUNT() FROM read_csv('{file_path}')").pl()[
        0, 0
    ]
    return current_count + 1
