import os
import re
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Optional, Sequence, Iterable

sys.path.append(os.path.join(os.getcwd()))
from pygolf.pygolfer import Pygolfer


class Example:
    shorten_suffix: str = "_shorten.py"

    def __init__(self, path):
        self.path: str = path
        self.shorten_path: str = re.sub("\\.py$", self.shorten_suffix, path)
        self.example_length: Optional[int] = None
        self.example_shortened_length: Optional[int] = None
        self.name = os.path.basename(path).split(".")[0]

    def shorten_code(self, pygolfer: Pygolfer):
        with open(self.path, "r") as input_fp, open(self.shorten_path, "w") as output_fp:
            code = input_fp.read()
            self.example_length = len(code)
            code_shortened = pygolfer.shorten(code)
            self.example_shortened_length = len(code_shortened)
            output_fp.write(code_shortened)

    def check_shorten_code(self, pygolfer: Pygolfer) -> bool:
        if not os.path.exists(self.shorten_path):
            return False
        with open(self.path, "r") as input_fp, open(self.shorten_path, "r") as output_fp:
            code = input_fp.read()
            self.example_length = len(code)
            code_shortened = pygolfer.shorten(code)
            self.example_shortened_length = len(code_shortened)
            code_previously_shortened = output_fp.read()
        return code_shortened == code_previously_shortened

    def __repr__(self) -> str:
        return os.path.basename(self.path)


def parse_arguments(argv: Optional[Sequence[str]] = None) -> Namespace:
    parser: ArgumentParser = ArgumentParser(description="PyGolf shortens a Python code")
    action_input = parser.add_mutually_exclusive_group()
    action_input.add_argument(
        "-c", "--check", help="Check whether the `_shorten` files are generated correctly", action="store_true",
    )

    action_input.add_argument(
        "-g", "--generate", help="Generate shorten_code of examples in folder `code_example`", action="store_true",
    )
    return parser.parse_args(argv)


def to_markdown_line(line: Iterable[str]):
    return "| " + " | ".join(line) + " |"


def main(argv: Optional[Sequence[str]] = None):
    arguments = parse_arguments(argv)

    examples_path = os.path.join(os.getcwd(), "code_example")

    statistics_path = os.path.join(examples_path, "README.md")

    examples: List[Example] = []

    for file in os.listdir(examples_path):

        example_path = os.path.join(examples_path, file)
        if file.endswith(".py") and not file.endswith(Example.shorten_suffix):
            examples.append(Example(example_path))

    pygolfer = Pygolfer()

    statistics: List[str] = [
        to_markdown_line(("example name", "example length", "example shortened length")),
        to_markdown_line(["---"] * 3),
    ]

    if arguments.generate:
        for example in examples:
            example.shorten_code(pygolfer)
            print(f"Shortened code {example.path}")
            statistics.append(
                to_markdown_line(map(str, (example.name, example.example_length, example.example_shortened_length)))
            )
        with open(statistics_path, "w") as fp:
            fp.write("\n".join(statistics))
        print("Statistics generated")

    elif arguments.check:
        examples_not_shortened_correctly: List[Example] = []
        for example in examples:
            if not example.check_shorten_code(pygolfer):
                examples_not_shortened_correctly.append(example)
            statistics.append(
                to_markdown_line(map(str, (example.name, example.example_length, example.example_shortened_length)))
            )

        with open(statistics_path, "r") as fp:
            generated_statistics = fp.read()

        if examples_not_shortened_correctly:
            print("The following examples have not been shortened correctly:")
            for example in examples_not_shortened_correctly:
                print("Expected, ", example, ":", sep="")
                with open(example.path, "r") as fp:
                    print(pygolfer.shorten(fp.read()))
            sys.exit(1)
        elif generated_statistics != "\n".join(statistics):
            print("Statistics have not been generated")
            print("Expected statistics", "\n" + "\n".join(statistics))
        else:
            print("All examples and statistics have been shortened.")


if __name__ == "__main__":
    main()
