class Python2CodeDetected(Exception):
    def __init__(self, node):
        super().__init__(f"Pygolf only reduces python 3 code, however {node} has been found in AST.")
