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

    def test_op_2(self):
        insert = "(+ 6 3)"
        should_be = "9"
        self.assert_eval(insert, should_be)

    def test_op_3(self):
        insert = "(+ 3 (* 5 6))"
        should_be = "33"
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

    def test_basic_4(self):
        insert = "(CAR '(X Y Z))"
        should_be = "X"
        self.assert_eval(insert, should_be)
        insert = "(CAR '((X) Y Z))"
        should_be = "(X)"
        self.assert_eval(insert, should_be)

    def test_basic_5(self):
        insert = "(CDR '(X Y Z))"
        should_be = "(Y Z)"
        self.assert_eval(insert, should_be)

    def test_basic_6(self):
        insert = "(SETQ X '(1 2 3))"
        should_be = "(1 2 3)"
        self.assert_eval(insert, should_be)
        insert = "(CAR (CDR (CDR X)))"
        should_be = "3"
        self.assert_eval(insert, should_be)
        insert = "(CADDR X)"
        should_be = "3"
        self.assert_eval(insert, should_be)

    def test_basic_7(self):
        insert = "(NTH 4 '(0 1 2 3 4 5 6))"
        should_be = "4"
        self.assert_eval(insert, should_be)
        insert = "(NTH 3 '(A B))"
        should_be = "NIL"
        self.assert_eval(insert, should_be)
        insert = "(NTH 3 'A)"
        should_be = "ERROR"
        self.assert_eval(insert, should_be)

    def test_basic_8(self):
        insert = "(CONS 'A '(B C D))"
        should_be = "(A B C D)"
        self.assert_eval(insert, should_be)
        insert = "(CONS '(E) '(1 2 3))"
        should_be = "((E) 1 2 3)"
        self.assert_eval(insert, should_be)

    def test_basic_9(self):
        insert = "(REVERSE '(A B C D))"
        should_be = "(D C B A)"
        self.assert_eval(insert, should_be)

    def test_basic_10(self):
        insert = "(APPEND '(A C) '(B D) '(E F))"
        should_be = "(A B C D E F)"
        self.assert_eval(insert, should_be)

    def test_basic_11(self):
        insert = "(LENGTH '(A B C))"
        should_be = "3"
        self.assert_eval(insert, should_be)
        insert = "(LENGTH '((A B C)))"
        should_be = "1"
        self.assert_eval(insert, should_be)

    def test_basic_12(self):
        insert = "(SETQ CLUB '(TOM HARRY JOHN DANIEL))"
        should_be = "(TOM HARRY JOHN DANIEL)"
        self.assert_eval(insert, should_be)
        insert = "(MEMBER 'HARRY CLUB)"
        should_be = "(HARRY JOHN DANIEL)"
        self.assert_eval(insert, should_be)

    def test_basic_13(self):
        insert = "(ASSOC 'TWO '((ONE 1)(TWO 2)(THREE 3)))"
        should_be = "(TWO 2)"
        self.assert_eval(insert, should_be)

    def test_basic_14(self):
        insert = "(SETQ MYLIST '(A B C D E F))"
        should_be = "(A B C D E F)"
        self.assert_eval(insert, should_be)
        insert = "(REMOVE 'D MYLIST)"
        should_be = "(A B C E F)"
        self.assert_eval(insert, should_be)
        insert = "(SETQ MYLIST '(A D B C D E D F))"
        should_be = "(A D B C D E D F)"
        self.assert_eval(insert, should_be)
        insert = "(REMOVE 'D MYLIST)"
        should_be = "(A B C E F)"
        self.assert_eval(insert, should_be)

    def test_basic_15(self):
        insert = "(SUBST 'GOOD 'BAD '(I AM BAD))"
        should_be = "(I AM GOOD)"
        self.assert_eval(insert, should_be)


class PredicateFunctionsTest(InterpreterTest):
    def test_predeciate_1(self):
        insert = '(STRINGP "A")'
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_2(self):
        insert = "(STRINGP #\A)"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_3(self):
        insert = "(STRINGP '(A B C))"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_4(self):
        insert = "(STRINGP 1.2)"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_5(self):
        insert = "(STRINGP 'A)"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_6(self):
        insert = "(STRINGP #(0 1 2))"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_7(self):
        insert = "(STRINGP NIL)"
        should_be = "NIL"
        self.assert_eval(insert, should_be)

    def test_predeciate_8(self):
        insert = '(STRINGP "HI THERE")'
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_9(self):
        insert = "(>= 5 2)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_10(self):
        insert = "(EQUAL 5 5)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_11(self):
        insert = "(MINUSP -2)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_12(self):
        insert = "(ZEROP 0)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_13(self):
        insert = "(NUMBERP 25)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_14(self):
        insert = "(NULL NIL)"
        should_be = "T"
        self.assert_eval(insert, should_be)

    def test_predeciate_15(self):
        insert = "(ATOM 'A)"
        should_be = "T"
        self.assert_eval(insert, should_be)


class ConditionalFunctionsTest(InterpreterTest):
    def test_conditional_1(self):
        insert = "(SETQ X 5)"
        should_be = "5"
        self.assert_eval(insert, should_be)
        insert = "(IF (> X 3) (PRINT X) (+ X 5))"
        should_be = "5"
        self.assert_eval(insert, should_be)


if __name__ == "__main__":
    unittest.main()