class atom:
    """ADT for atom"""

    def __init__(self, value):
        self.value = value.strip("'")

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return (
            True
            if isinstance(other, self.__class__) and other.value == self.value
            else False
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class string:
    """ADT for string"""

    def __init__(self, value):
        self.value = value.strip("'")

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return string(
            '"' + str(self.value.strip('"')) + str(other.value.strip('"')) + '"'
        )

    def __eq__(self, other):
        return (
            True
            if isinstance(other, self.__class__) and other.value == self.value
            else False
        )


class nil(object):
    """ADT for nil """

    def __repr__(self):
        return "NIL"

    def __str__(self):
        return "NIL"

    def __len__(self):
        return 0

    def __bool__(self):
        return False

    def __getitem__(self, k):
        raise IndexError("Index out of bound")

    def __eq__(self, other):
        if isinstance(other, nil):
            return True
        return False


nil = nil()  # Assignment hides the nil class; there is only one instance

# class number_p()