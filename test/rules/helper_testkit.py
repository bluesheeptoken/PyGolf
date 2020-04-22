from contextlib import contextmanager

from astroid.transforms import TransformVisitor

from pygolf.rules import AstroidRule


@contextmanager
def register_rule(rule: AstroidRule) -> None:
    transformer: TransformVisitor = TransformVisitor()
    transformer.register_transform(
        rule.on_node, rule.transform, rule.predicate,
    )
    yield transformer
