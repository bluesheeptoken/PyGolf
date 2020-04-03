import unittest

import astroid

from pygolf.rules.format_to_f_string import FormatToFString
from pygolf.unparser import Unparser


class TestFormatToFString(unittest.TestCase):
    format_to_f_string_rule = FormatToFString()
    astroid.MANAGER.register_transform(
        format_to_f_string_rule.on_node,
        format_to_f_string_rule.transform,
        format_to_f_string_rule.predicate,
    )

    def test_rule(self):
        node = astroid.extract_node(
            "'The best {} version is {:.2f}'.format(language, version)"
        )

        unparser = Unparser()

        self.assertEqual(
            "f'The best {language} version is {version:.2f}'", unparser.unparse(node)
        )
