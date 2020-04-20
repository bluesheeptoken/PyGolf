import os
import re
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Optional, Sequence

sys.path.append(os.path.join(os.getcwd()))
from pygolf.pygolfer import Pygolfer


class Example:
    shorten_suffix: str = "_shorten.py"

    def __init__(self, path):
        self.path: str = path
        self.shorten_path: str = re.sub("\\.py$", self.shorten_suffix, path)

    def shorten_code(self, pygolfer: Pygolfer):
        with open(self.path, "r") as input_fp, open(
            self.shorten_path, "w"
        ) as output_fp:
            code = input_fp.read()
            code_shortened = pygolfer.shorten(code)
            output_fp.write(code_shortened)

    def check_shorten_code(self, pygolfer: Pygolfer) -> bool:
        if not os.path.exists(self.shorten_path):
            return False
        with open(self.path, "r") as input_fp, open(
            self.shorten_path, "r"
        ) as output_fp:
            code = input_fp.read()
            code_shortened = pygolfer.shorten(code)
            code_previously_shortened = output_fp.read()
        return code_shortened == code_previously_shortened


def parse_arguments(argv: Optional[Sequence[str]] = None) -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="PyGolf shortens a Python code")
    action_input = parser.add_mutually_exclusive_group()
    action_input.add_argument(
        "-c",
        "--check",
        help="Check whether the `_shorten` files are generated correctly",
        action="store_true",
    )

    action_input.add_argument(
        "-g",
        "--generate",
        help="Generate shorten_code of examples in folder `code_example`",
        action="store_true",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None):
    arguments = parse_arguments(argv)

    examples_path = os.path.join(os.getcwd(), "code_example")

    examples: List[Example] = []

    for file in os.listdir(examples_path):

        example_path = os.path.join(examples_path, file)
        if file.endswith(".py") and not file.endswith(Example.shorten_suffix):
            examples.append(Example(example_path))

    pygolfer = Pygolfer()

    if arguments.generate:
        for example in examples:
            example.shorten_code(pygolfer)
            print(f"Shortened code {example.path}")
    elif arguments.check:
        examples_not_shortened_correctly = [
            example for example in examples if not example.check_shorten_code(pygolfer)
        ]
        if examples_not_shortened_correctly:
            print(
                "The following examples have not been shortened correctly:",
                {
                    ", ".join(
                        example.path for example in examples_not_shortened_correctly
                    )
                },
            )
            sys.exit(1)
        else:
            print("All examples have been shortened.")


if __name__ == "__main__":
    main()
