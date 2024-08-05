

class IsNotGyatDirError(Exception):

    def __str__(self) -> str:
        return "Current directory not a gyat directory!"


class IsNotSameTypeError(Exception):
    def __init__(self, object_type: str, given_object_type):
        if object_type:
            self.message = (f"Object type what was given: {given_object_type}"
                            f" is not {object_type}!")
        else:
            self.message = None


class NotValidShaOrTagOrRef(Exception):

    def __str__(self) -> str:
        return "Not valid sha or Tag or Ref!"


class NecessaryArgsError(Exception):
    def __init__(self, message: str):
        if message:
            self.message = f"Object: {message} is not Tree!"
        else:
            self.message = None
