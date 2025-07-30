from typing import List

from InputPowertools import cli


def test_cli(a, b: str, c: List[str], d: bool = False):
    """
    Some function

    A function that is truly amazing... wow!

    :param a: Is a variable called a
    :param b: Is a variable called b
    :param c: Is a variable called c
    :param d: Is a variable called d
    :return: Some fascinating thing
    """
    print(f'{a=} {b=} {c=} {d=}')


if __name__ == '__main__':
    cli.run(test_cli)
    # run python example 1.py
    # run python example 1.py --help
    # run python example 1.py --a lol --b "this is a value with spaces" --c 4 2 "test123" --d
