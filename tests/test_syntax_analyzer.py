import unittest
from src.components.lexer import Lexer
from src.components.syntax_analyzer import Parser


lexer = Lexer()
parser = Parser()


class TestProgramAbstraction(unittest.TestCase):
    def test_empty_program(self):
        lexemes = lexer.process(
            """HAI
        KTHXBYE"""
        )

        try:
            parser.parse(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")

    def test_no_hai(self):
        lexemes = lexer.process("KTHXBYE")

        with self.assertRaises(SyntaxError):
            parser.parse(lexemes)

    def test_no_kthxbye(self):
        lexemes = lexer.process("HAI")

        with self.assertRaises(SyntaxError):
            parser.parse(lexemes)

    def test_no_newlines(self):
        lexemes = lexer.process("HAI KTHXBYE")

        with self.assertRaises(SyntaxError):
            parser.parse(lexemes)

        lexemes = lexer.process(
            """HAI
        VISIBLE 1 KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.parse(lexemes)

        lexemes = lexer.process(
            """HAI VISIBLE 1
        KTHXBYE"""
        )

        with self.assertRaises(SyntaxError):
            parser.parse(lexemes)


class TestLoopAbstraction(unittest.TestCase):
    def test_loop(self):
        lexemes = lexer.process(
            """HAI
            IM IN YR asc UPPIN YR num2 WILE BOTH SAEM num2 AN SMALLR OF num2 AN num1
                VISIBLE num2
            IM OUTTA YR asc
        KTHXBYE"""
        )

        try:
            parser.parse(lexemes)
        except SyntaxError:
            self.fail("Unexpected syntax error")
