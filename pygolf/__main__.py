import sys
from argparse import ArgumentParser, Namespace
from typing import *

import pyperclip  # type: ignore
from astroid import AstroidSyntaxError

from pygolf.pygolfer import Pygolfer


def stdout_output_message(old_code: str, new_code: str) -> str:
    return f"""Shortened code:
---
{new_code}
---
Saved {len(old_code) - len(new_code)} characters
The reduced code has {len(new_code)} characters
"""


def reduce(code: str) -> Optional[str]:
    pygolfer = Pygolfer()
    try:
        return pygolfer.reduce(code)
    except AstroidSyntaxError:
        return None


def read_input_code(arguments: Namespace) -> str:
    if arguments.clipboard:
        return pyperclip.paste()  # type: ignore
    elif arguments.code is not None:
        return arguments.code  # type: ignore
    with open(arguments.input_file) as fp:
        return "".join(fp.readlines())


def output_code(arguments: Namespace, old_code: str, new_code: Optional[str]) -> None:
    if new_code is None:
        print("Input code is not a valid python code")
    elif arguments.clipboard:
        pyperclip.copy(new_code)
    elif arguments.code is not None:
        print(stdout_output_message(old_code, new_code))
    elif arguments.input_file is not None:
        if arguments.output_file:
            with open(arguments.output_file, "w") as fp:
                fp.write(new_code)
        else:
            print(stdout_output_message(old_code, new_code))


def get_arguments_warning(arguments: Namespace) -> Iterable[str]:
    if arguments.input_file is None and arguments.output_file is not None:
        yield "argument `output_file` is set but not `input_file`, ignoring argument `output_file`"


def parse_arguments(argv: Optional[Sequence[str]] = None) -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="PyGolf shortens a Python code")
    code_input_group = parser.add_mutually_exclusive_group()
    code_input_group.add_argument(
        "-c", "--code", help="Shorten code from argument and print it", type=str,
    )

    code_input_group.add_argument(
        "-cb", "--clipboard", help="Shorten code in clipboard", action="store_true",
    )

    code_input_group.add_argument(
        "-i",
        "--input_file",
        help="Shorten code from file code and print it to stdout or to --output_file",
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output_file",
        help="Outputs the code to given output_file or stdout by default",
        nargs="?",
    )

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    arguments = parse_arguments(argv)

    for warning in get_arguments_warning(arguments):
        print(warning)

    input_code = read_input_code(arguments)

    reduced_code = reduce(input_code)

    output_code(arguments, input_code, reduced_code)


if __name__ == "__main__":
    main()
