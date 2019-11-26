class ShouldBeReducedException(Exception):
    def __init__(self, detected_keyword):
        super().__init__(
            f"Pygolf only reduces python 3 code, however {detected_keyword} was seen in the code."
        )
