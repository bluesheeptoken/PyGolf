class Python2CodeDetected(Exception):
    def __init__(self, node):
        super().__init__(
            f"{node} is supposed to be reduced by the golfer, please report a bug."
        )
