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

        parser.parse(lexemes)

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
