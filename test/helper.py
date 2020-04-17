from contextlib import contextmanager

import astroid as ast

from pygolf.rules import AstroidRule


@contextmanager
def register_rule(rule: AstroidRule) -> None:
    ast.MANAGER.register_transform(
        rule.on_node, rule.transform, rule.predicate,
    )
    yield None
    ast.MANAGER.unregister_transform(
        rule.on_node, rule.transform, rule.predicate,
    )
