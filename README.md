# PyGolf

PyGolf is a python code shortener.

PyGolf takes a valid python code as input and outputs an equivalent code with fewer characters.

You can find examples of reduced code in the folder [code_example](code_example). These examples mainly come from [CodinGame](https://www.codingame.com/home)'s Clash of Code game.

## Getting Started

### Installing

You can install this project directly from pypi with `pip install pygolf`

### How to use it

You can call it using either `pygolf` or `python -m pygolf`.

You can:
 - Give some code with `-c`, `pygolf -c "print( 2 )"`
 - Give an input and output file, `pygolf -i input_file -o output_file`
 - Shorten code in clipboard with `pygolf -cb` (usefull while doing a clash of code)

To modify the clipboard, `pygolf` requires [pyperclip](https://pypi.org/project/pyperclip/). You might have some issues such as `Could not find a copy/paste mechanism for your system`. If so, refer to [pyperclip guidelines](https://github.com/asweigart/pyperclip/blob/master/README.md).

### How does it work

`PyGolf` uses [astroid]() to parse and apply transformations on the abstract syntax tree (AST).

`PyGolf` parses and unparses the AST several times through [phases](pygolf/optimization_phases). Each phase comes with [rules](pygolf/rules).

If you want to contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.
