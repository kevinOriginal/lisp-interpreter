class BaseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[RuntimeError] : %s" % self.message


class ArgumentsError(BaseException):
    def __str__(self):
        return "[ArgumentsError] : %s" % self.message


class DuplicateError(BaseException):
    def __str__(self):
        return "[DuplicateError] : %s" % self.messag


class UndefinedError(BaseException):
    def __str__(self):
        return "[UndefinedError] : %s" % self.message


class TypeError(BaseException):
    def __str__(self):
        return "[TypeError] : %s" % self.message


class BoundError(BaseException):
    def __str__(self):
        return "[BoundError] : %s" % self.message
