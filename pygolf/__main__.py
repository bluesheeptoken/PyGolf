from argparse import ArgumentParser, Namespace
from typing import *

import pyperclip  # type: ignore

from pygolf.pygolfer import Pygolfer


def stdout_output_message(old_code: str, new_code: str) -> str:
    return f"""Reduced code:
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
    except:
        return None


def read_input_code(arguments: Namespace) -> str:
    if arguments.clipboard:
        return pyperclip.paste()  # type: ignore
    elif arguments.code is not None:
        return arguments.code  # type: ignore
    with open(arguments.input_path) as fp:
        return "".join(fp.readlines())


def output_code(arguments: Namespace, old_code: str, new_code: Optional[str]) -> None:
    if new_code is None:
        print("Input code is not a valid python code")
    elif arguments.clipboard:
        pyperclip.copy(new_code)
    elif arguments.code is not None:
        print(stdout_output_message(old_code, new_code))
    elif arguments.input_path is not None:
        if arguments.output_path:
            with open(arguments.output_path, "w") as fp:
                fp.write(new_code)
        else:
            print(stdout_output_message(old_code, new_code))


def get_arguments_warning(arguments: Namespace) -> List[str]:
    warnings: List[str] = []

    if arguments.input_path is None and arguments.output_path is not None:
        warnings.append(
            "argument `output_path` is set but not `input_path`, ignoring argument `output_path`"
        )

    return warnings


def parse_arguments(argv: Optional[Sequence[str]] = None) -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="PyGolf reduces the text")
    code_input_group = parser.add_mutually_exclusive_group()
    code_input_group.add_argument(
        "-c",
        "--code",
        help="Reduce code from argument and prints it in the stout",
        type=str,
    )

    code_input_group.add_argument(
        "-cb",
        "--clipboard",
        help="Reduce code from clipboard and save it in clipboard",
        action="store_true",
    )

    code_input_group.add_argument(
        "-i",
        "--input_path",
        help="Reduce code from clipboard and prints it to stdout or to --output_path",
        type=str,
    )

    parser.add_argument(
        "-o",
        "--output_path",
        help="Outputs the code to given output_path or stdout by default",
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
