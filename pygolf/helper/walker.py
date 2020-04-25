from astroid.node_classes import NodeNG


def walk(node: NodeNG):
    yield node
    yield from _visit(node)


def _visit(node: NodeNG):
    if hasattr(node, "_astroid_fields"):
        for name in node._astroid_fields:
            value = getattr(node, name)
            yield from _visit_generic(value)


def _visit_generic(node: NodeNG):
    if isinstance(node, list) or isinstance(node, tuple):
        for child in node:
            yield child
            yield from _visit(child)
    elif not node or isinstance(node, str):
        pass
    else:
        yield node
    yield from _visit(node)
