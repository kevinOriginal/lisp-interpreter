#  Atom type을 새로 생성
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


# Atom과의 구별을 위해 기존 python의 str 타입 말고 새로운 string data type을 새로 만들었다.
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


# 따로 Nil Type을 만들어주었다.
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


# nil이 존재하는 변수처럼 써주기 위한 처리 방법
nil = nil()
