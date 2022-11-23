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

        output = self._Output()
        if output is not None:
            statements.append(output)

        return statements

    def _Declaration(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.VARIABLE_DECLARATION:
            return
        body.append(self.lexemes.pop(0))

        if self._lookahead().lexemeType is not TOKEN.VARIABLE_IDENTIFIER:
            return
        body.append(self.lexemes.pop(0))

        if self._lookahead().lexemeType is not TOKEN.VARIABLE_ASSIGNMENT:
            return Node(ABSTRACTION.DECLARATION, body)
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is None:
            self._throwSyntaxError("Needs value")
        body.append(operand)

        return Node(ABSTRACTION.DECLARATION, body)

    def _Output(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.OUTPUT_KEYWORD:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is None:
            return
        body.append(operand)

        return Node(ABSTRACTION.OUTPUT, body)

    def _Operand(self):
        literal = self._Literal()
        if literal is not None:
            return Node(ABSTRACTION.OUTPUT, literal)

        if self._lookahead().lexemeType is TOKEN.VARIABLE_IDENTIFIER:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        return
    
    def _Literal(self):
        if self._lookahead().lexemeType is TOKEN.BOOL_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)
        
        if self._lookahead().lexemeType is TOKEN.FLOAT_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.INTEGER_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.TYPE_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        return

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
