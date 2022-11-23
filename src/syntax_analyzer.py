from abstractions import ABSTRACTION
from token_enum import TOKEN


class Parser:
    def parse(self, lexemes):
        self.lexemes = lexemes

        return self._Program()

    def _lookahead(self):
        return self.lexemes[0]

    def _Program(self):
        if self._lookahead().lexemeType is not TOKEN.CODE_DELIMITER:
            self._throwSyntaxError('Missing starting keyword "HAI"')
        self.lexemes.pop(0)

        statements = self._Statements()

        if len(statements) == 0:
            self._throwSyntaxError("Expected statements")

        # if self._lookahead().lexemeType is not TOKEN.CODE_DELIMITER:
        #     self._throwSyntaxError('Missing ending keyword "KTHXBYE"')

        return Node(ABSTRACTION.PROGRAM, statements)

    def _Statements(self):
        statements = []

        declaration = self._Declaration()
        if declaration is not None:
            statements.append(declaration)

        return statements

    def _Declaration(self):
        if self._lookahead().lexemeType is not TOKEN.VARIABLE_DECLARATION:
            return
        self.lexemes.pop(0)

        if self._lookahead().lexemeType is not TOKEN.VARIABLE_IDENTIFIER:
            return
        self.lexemes.pop(0)

        # if self._lookahead().lexemeType is TOKEN.VARIABLE_ASSIGNMENT:
        #     if self._lookahead().lexemeType is not TOKEN.

        return Node(ABSTRACTION.DECLARATION, "I HAS A @1")

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            None,
            0,
            None,
        )

        # raise SyntaxError(message, syntaxErrorArgs)


class Node:
    def __init__(self, type, body):
        self.type = type
        self.body = body
