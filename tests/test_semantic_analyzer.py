import unittest
from src.components.lexer import Lexer
from src.components.syntax_analyzer import Parser


lexer = Lexer()
parser = Parser()


class TestDeclarationAbstraction(unittest.TestCase):
    def test_valid_declaration(self):
        lexemes = lexer.process(
            """HAI
            I HAS A var
        KTHXBYE"""
        )

        parser.parse(lexemes)
        self.assertIsNone(parser.memory["var"])

    def test_valid_declaration_with_value(self):
        lexemes = lexer.process(
            """HAI
            I HAS A var ITZ 5
        KTHXBYE"""
        )

        parser.parse(lexemes)
        self.assertEqual(parser.memory["var"], 5)
