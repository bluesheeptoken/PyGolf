import argparse

from pygolf.pygolfer import Pygolfer


def main():
    parser = argparse.ArgumentParser(description="Run pygolf")
    parser.add_argument("--file_path", dest="file_path", help="path of file to reduce")

    args = parser.parse_args()

    reducer = Pygolfer()

    with open(args.file_path) as f:
        old_code = "".join(f.readlines())

    reduced_code = reducer.reduce(args.file_path)

    print("## Old code ##")
    print(old_code)
    print()
    print("## Reduced code ##")
    print()
    print(reduced_code)
    print()
    print("## Characters saved ##")
    print()
    old_number_characters = len(old_code)
    new_number_characters = len(reduced_code)
    characters_saved = old_number_characters - new_number_characters

    print(
        f"""Previous code had {old_number_characters} characters
    New code has {new_number_characters} characters
    {characters_saved} characters saved ({characters_saved / old_number_characters * 100:.2f}%)"""
    )


if __name__ == "__main__":
    main()
