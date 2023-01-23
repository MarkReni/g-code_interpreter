import argparse
from typing import Union


# Auxiliary functions
def arg_parser() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("gcode_file", type=str)

    args = parser.parse_args()

    file_name = args.gcode_file
    print("A file with the following ending has been added:", file_name[-5:])

    return file_name


def error_check(literal: str) -> Union[float, int]:
    try:
        conversion = float(literal)
    except ValueError:
        try:
            conversion = int(literal)
        except ValueError:
            raise Exception("Gcode syntax incorrect: Some value is not recognized as float/int.")
        else:
            return conversion
    else:
        return conversion


def change_datum(datum: tuple, x: int, y: int, z: int) -> tuple:
    X, Y, Z = x + datum[0], y + datum[1], z + datum[2]
    return X, Y, Z
