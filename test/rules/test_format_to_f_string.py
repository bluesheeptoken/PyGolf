import unittest

import astroid

from pygolf.rules.format_to_f_string import FormatToFString
from pygolf.unparser import Unparser


class TestFormatToFString(unittest.TestCase):
    astroid.MANAGER.register_transform(
        FormatToFString.on_node, FormatToFString.transform, FormatToFString.predicate
    )

    def test_rule(self):
        node = astroid.extract_node(
            "'The best {} version is {:.2f}'.format(language, version)"
        )

        unparser = Unparser()

        self.assertEqual(
            unparser.unparse(node), "f'The best {language} version is {version:.2f}'"
        )
