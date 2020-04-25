class NoNamesLeftException(Exception):
    def __init__(self):
        super().__init__("No name left to optimize code")
