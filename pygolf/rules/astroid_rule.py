class AstroidRule:
    def transform(self, node):
        raise NotImplementedError

    def predicate(self, node):
        raise NotImplementedError

    def since(self):
        raise NotImplementedError
