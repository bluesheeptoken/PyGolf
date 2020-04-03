class Version:
    def __init__(self, version: str) -> None:
        major, minor, *_ = version.split(".")
        self.major: int = int(major)
        self.minor: int = int(minor)
