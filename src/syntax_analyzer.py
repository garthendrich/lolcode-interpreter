from abstractions import ABSTRACTION
from token_enum import TOKEN


class Parser:
    def parse(self, lexemes):
        self.lexemes = lexemes

        return self._Program()

    def _Program(self):
        lexeme = self.lexemes.pop(0)
        if lexeme.lexemeType is not TOKEN.CODE_DELIMITER:
            self._throwSyntaxError('Missing starting keyword "HAI"')

        statements = self._Statements()

        # lexeme.lexemeType = self.lexemes.pop(0)
        # if lexeme is not TOKEN.CODE_DELIMITER:
        #     self._throwSyntaxError('Missing ending keyword "KTHXBYE"')

        return Node(ABSTRACTION.PROGRAM, statements)

    def _Statements(self):
        return []

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            None,
            0,
            None,
        )

        raise SyntaxError(message, syntaxErrorArgs)


class Node:
    def __init__(self, type, body):
        self.type = type
        self.body = body
