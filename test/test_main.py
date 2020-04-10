import argparse
import tempfile
import unittest

import pyperclip  # type: ignore

from pygolf.__main__ import get_arguments_warning, read_input_code, reduce


class TestMain(unittest.TestCase):
    def test_reduce(self):
        self.assertEqual(reduce("print( 1 + 2 )"), "print(1+2)")
        self.assertEqual(reduce("not valid code"), None)

    def test_read_input_code(self):
        name_space = argparse.Namespace()
        name_space.code = None
        name_space.clipboard = None
        name_space.input_path = None

        name_space.code = "print('code')"
        self.assertEqual(read_input_code(name_space), "print('code')")
        name_space.code = None

        name_space.clipboard = True
        old_text_in_cb = pyperclip.paste()
        pyperclip.copy("print('pyperclip')")
        self.assertEqual(read_input_code(name_space), "print('pyperclip')")
        pyperclip.copy(old_text_in_cb)
        name_space.clipboard = None

        with tempfile.NamedTemporaryFile("w+") as fp:
            fp.write("print('input_path')")
            fp.flush()
            name_space.input_path = fp.name
            self.assertEqual(read_input_code(name_space), "print('input_path')")
            name_space.input_path = None

    def test_get_arguments_warning(self):
        name_space = argparse.Namespace()
        name_space.input_path = None
        name_space.output_path = "path"
        self.assertEqual(len(get_arguments_warning(name_space)), 1)
