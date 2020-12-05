class atom:
    """ADT for atom"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, compare):
        return (
            True
            if isinstance(compare, self.__class__) and compare.value == self.value
            else False
        )


class nil(object):
    """ADT for nil """

    def __repr__(self):
        return "<nil> "

    def __str__(self):
        return "nil"

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