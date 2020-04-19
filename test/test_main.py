import argparse
import tempfile
import unittest

from pygolf.__main__ import get_arguments_warning, read_input_code, shorten


class TestMain(unittest.TestCase):
    def test_reduce(self):
        self.assertEqual(shorten("print( 1 + 2 )"), "print(1+2)")
        self.assertEqual(shorten("not valid code"), None)

    def test_read_input_code(self):
        name_space = argparse.Namespace()
        name_space.code = None
        name_space.clipboard = None
        name_space.input_file = None

        name_space.code = "print('code')"
        self.assertEqual(read_input_code(name_space), "print('code')")
        name_space.code = None

        with tempfile.NamedTemporaryFile("w+") as fp:
            fp.write("print('input_file')")
            fp.flush()
            name_space.input_file = fp.name
            self.assertEqual(read_input_code(name_space), "print('input_file')")
            name_space.input_file = None

    def test_get_arguments_warning(self):
        name_space = argparse.Namespace()
        name_space.input_file = None
        name_space.output_file = "path"
        self.assertEqual(len(list(get_arguments_warning(name_space))), 1)
