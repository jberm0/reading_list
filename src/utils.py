import polars as pl
from typing import Dict, List

class Args:
    def __repr__(self):
        return str(vars(self))

def get_arguments_input(argument_names: List[str]):
    args = Args()

    for arg_name in argument_names:
        arg_val = input(f'>>> enter {arg_name}: ')
        setattr(args, arg_name, arg_val)

    return args