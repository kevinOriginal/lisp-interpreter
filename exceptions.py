class LispException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[RuntimeError] : %s" % self.message


class ArgumentsError(LispException):
    def __str__(self):
        return "[ArgumentsError] : %s" % self.message


class DuplicateError(LispException):
    def __str__(self):
        return "[DuplicateError] : %s" % self.messag


class UndefinedError(LispException):
    def __str__(self):
        return "[UndefinedError] : %s" % self.message


class TypeError(LispException):
    def __str__(self):
        return "[TypeError] : %s" % self.message


class BoundError(LispException):
    def __str__(self):
        return "[BoundError] : %s" % self.message
