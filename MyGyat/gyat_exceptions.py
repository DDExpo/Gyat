

class IsNotCommitError(Exception):
    def __init__(self, sha_path: str):
        if sha_path:
            self.message = f"Object: {sha_path} is not Commit!"
        else:
            self.message = None


class IsNotTreeError(Exception):
    def __init__(self, sha_path: str):
        if sha_path:
            self.message = f"Object: {sha_path} is not Tree!"
        else:
            self.message = None
