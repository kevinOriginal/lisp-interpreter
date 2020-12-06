import unittest
import sys
from io import StringIO
from main import interpret
from exceptions import UndefinedError


class InterpreterTest(unittest.TestCase):
    def setUp(self):
        self.env = {}

    def assert_eval(self, insert, should_be):
        result = interpret(insert, self.env)
        self.assertEqual(result, should_be)

    def assert_raise(self, insert, should_be):
        with self.assertRaises(should_be):
            interpret(insert, self.env)


class OperationTest(InterpreterTest):
    def test_op_1(self):
        insert = "(SETQ X 3)"
        should_be = "3"
        self.assert_eval(insert, should_be)


class BasicFunctionsTest(InterpreterTest):
    def test_basic_1(self):
        insert = "(LIST 'X X 'Y)"

    def test_basic_2(self):
        insert = "(LIST 'X X 'Y)"
        self.assert_raise(insert, UndefinedError)

    def test_basic_3(self):
        insert = "(SETQ X 5)"
        should_be = "5"
        self.assert_eval(insert, should_be)
        insert = "(LIST 'X X 'Y)"
        should_be = "(X 5 Y)"
        self.assert_eval(insert, should_be)


if __name__ == "__main__":
    unittest.main()