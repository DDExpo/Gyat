

class IsNotCommitError(Exception):
    def __init__(self, sha_commit: str):
        if sha_commit:
            self.message = f"Object: {sha_commit} is not Commit!"
        else:
            self.message = None


class IsNotTreeError(Exception):
    def __init__(self, sha_tree: str):
        if sha_tree:
            self.message = f"Object: {sha_tree} is not Tree!"
        else:
            self.message = None
