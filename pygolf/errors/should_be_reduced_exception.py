class ShouldBeReducedException(Exception):
    def __init__(self, detected_keyword):
        super().__init__(
            f"{detected_keyword} is supposed to be reduced by the golfer, please report a bug."
        )
