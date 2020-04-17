from astroid.node_classes import NodeNG


class Optimizer:
    def visit(self, node: NodeNG):
        if hasattr(self, f"visit_{node.__class__.__name__}"):
            method = getattr(self, f"visit_{node.__class__.__name__}")
            method(node)

    def generate_rules(self):
        raise NotImplementedError
