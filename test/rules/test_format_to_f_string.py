import unittest
from test.rules.helper import register_rule

import astroid

from pygolf.rules import FormatToFString
from pygolf.unparser import Unparser


class TestFormatToFString(unittest.TestCase):
    def test_rule(self):
        unparser = Unparser()

        with register_rule(FormatToFString()):
            node = astroid.extract_node(
                "'The best {} version is {:.2f} !'.format(language, version)"
            )
            self.assertEqual(
                "f'The best {language} version is {version:.2f} !'",
                unparser.unparse(node),
            )
