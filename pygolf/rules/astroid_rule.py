class AstroidRule:
    def transform(self):
        raise NotImplementedError

    def predicate(self):
        raise NotImplementedError

    def since(self):
        raise NotImplementedError
