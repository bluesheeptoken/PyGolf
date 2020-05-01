import os
import re
import sys
from argparse import ArgumentParser, Namespace
from typing import List, Optional, Sequence, Iterable

sys.path.append(os.path.join(os.getcwd()))
from pygolf.pygolfer import Pygolfer


class Example:
    shorten_suffix: str = "_shorten.py"

    def __init__(self, path: str, pygolfer: Pygolfer):
        self.path: str = path
        self.path_shortened_code: str = re.sub("\\.py$", self.shorten_suffix, path)
        self.name = os.path.basename(path).split(".")[0]
        with open(self.path, "r") as input_fp:
            self.code: str = input_fp.read()
        self.shortened_code: str = pygolfer.shorten(self.code)

    def shorten_code(self) -> None:
        with open(self.path_shortened_code, "w") as output_fp:
            output_fp.write(self.shortened_code)

    def check_shorten_code(self) -> bool:
        if not os.path.exists(self.path_shortened_code):
            return False
        with open(self.path_shortened_code, "r") as output_fp:
            code_previously_shortened = output_fp.read()
        return self.shortened_code == code_previously_shortened

    def code_length(self) -> int:
        return len(self.code)

    def shortened_code_length(self) -> int:
        return len(self.shortened_code)

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
    pygolfer = Pygolfer()

    for file in sorted(os.listdir(examples_path)):

        example_path = os.path.join(examples_path, file)
        if file.endswith(".py") and not file.endswith(Example.shorten_suffix):
            examples.append(Example(example_path, pygolfer))

    statistics: List[str] = [
        to_markdown_line(("example name", "example length", "example shortened length")),
        to_markdown_line(["---"] * 3),
    ]

    for example in examples:
        statistics.append(to_markdown_line(map(str, (example.name, example.code_length(), example.shortened_code_length()))))

    if arguments.generate:
        for example in examples:
            example.shorten_code()
            print(f"Shortened code {example.path}")

        with open(statistics_path, "w") as fp:
            fp.write("\n".join(statistics))
        print("Statistics generated")

    elif arguments.check:
        examples_not_shortened_correctly: List[Example] = []
        for example in examples:
            if not example.check_shorten_code():
                examples_not_shortened_correctly.append(example)

        if not os.path.exists(statistics_path):
            print("statistics have not been generated")
            exit(1)

        with open(statistics_path, "r") as fp:
            generated_statistics = fp.read()

        if examples_not_shortened_correctly:
            print("The following example(s) have not been shortened correctly:")
            for example in examples_not_shortened_correctly:
                print("Expected, ", example, ":", sep="")
                with open(example.path, "r") as fp:
                    print(pygolfer.shorten(fp.read()))
            exit(1)
        elif generated_statistics != "\n".join(statistics):
            print("Statistics have not been generated")
            print("Expected statistics", "\n" + "\n".join(statistics))
            exit(1)
        else:
            print("All examples and statistics have been shortened.")


if __name__ == "__main__":
    main()
