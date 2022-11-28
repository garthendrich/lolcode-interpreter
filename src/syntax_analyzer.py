from abstractions import ABSTRACTION
from token_enum import TOKEN
from utils import isEmpty


class Parser:
    def parse(self, lexemes):
        self.lexemes = lexemes

        return self._Program()

    def _nextTokenIs(self, tokenType):
        return self.lexemes[0].lexemeType == tokenType

    def _popNext(self):
        return self.lexemes.pop(0)

    def _moveNextTokenTo(self, list):
        list.append(self._popNext())

    def _Program(self):
        children = []

        if self._nextTokenIs(TOKEN.CODE_DELIMITER):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.LINEBREAK):
                self._moveNextTokenTo(children)

                children.append(self._Statements())

                if self._nextTokenIs(TOKEN.CODE_DELIMITER):
                    self._moveNextTokenTo(children)

                    return Node(ABSTRACTION.PROGRAM, children)

                self._throwSyntaxError('Missing starting keyword "KTHXBYE"')

            self._throwSyntaxError("Unexpected keyword")

        self._throwSyntaxError('Missing starting keyword "HAI"')

    def _Statements(self):
        statement = self._Declaration() or self._Output() or self._TwoOperandOperation()

        if statement is None:
            self._throwSyntaxError("Statement error")

        children = [statement]

        if self._nextTokenIs(TOKEN.LINEBREAK):
            self._moveNextTokenTo(children)

            # if not yet end of source code
            if not self._nextTokenIs(TOKEN.CODE_DELIMITER):
                children.append(self._Statements())

            return Node(ABSTRACTION.STATEMENT, children)

        self._throwSyntaxError("Unexpected keyword")

    def _Declaration(self):
        children = []

        if self._nextTokenIs(TOKEN.VARIABLE_DECLARATION):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                    self._moveNextTokenTo(children)

                    operand = self._Operand()
                    if operand is None:
                        self._throwSyntaxError("Expected an expression")

                    children.append(operand)

                return Node(ABSTRACTION.DECLARATION, children)

            self._throwSyntaxError("Expected a variable identifier")

        return None

    # !! does not yet accept multiple operands
    def _Output(self):
        children = []

        if self._nextTokenIs(TOKEN.OUTPUT_KEYWORD):
            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is None:
                self._throwSyntaxError("Expected an operand")

            children.append(operand)
            return Node(ABSTRACTION.OUTPUT, children)

        return None

    def _Operand(self):
        literal = self._Literal()
        if literal is not None:
            return Node(ABSTRACTION.OPERAND, literal)

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            lexeme = self._popNext()
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        return None

    def _Literal(self):
        if (
            self._nextTokenIs(TOKEN.BOOL_LITERAL)
            or self._nextTokenIs(TOKEN.FLOAT_LITERAL)
            or self._nextTokenIs(TOKEN.INTEGER_LITERAL)
            or self._nextTokenIs(TOKEN.STRING_LITERAL)
            or self._nextTokenIs(TOKEN.TYPE_LITERAL)
            or self._nextTokenIs(TOKEN.STRING_LITERAL)
        ):
            lexeme = self._popNext()
            return Node(lexeme.lexemeType, lexeme.lexeme)

        return None

    # !!! does not yet accept nested operations
    def _TwoOperandOperation(self):
        children = []

        if (
            self._nextTokenIs(TOKEN.ADDITION_OPERATION)
            or self._nextTokenIs(TOKEN.SUBTRACTION_OPERATION)
            or self._nextTokenIs(TOKEN.MULTIPLICATION_OPERATION)
            or self._nextTokenIs(TOKEN.QUOTIENT_OPERATION)
            or self._nextTokenIs(TOKEN.MODULO_OPERATION)
            or self._nextTokenIs(TOKEN.MAX_OPERATION)
            or self._nextTokenIs(TOKEN.MIN_OPERATION)
            or self._nextTokenIs(TOKEN.AND_OPERATION)
            or self._nextTokenIs(TOKEN.OR_OPERATION)
            or self._nextTokenIs(TOKEN.XOR_OPERATION)
        ):
            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is not None:
                children.append(operand)

                if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                    self._moveNextTokenTo(children)

                    operand = self._Operand()
                    if operand is not None:
                        children.append(operand)

                        # !!! temporary node type
                        return Node("operation", children)

                    self._throwSyntaxError("Expected an operand")

                self._throwSyntaxError('Missing keyword "AN"')

            self._throwSyntaxError("Expected an operand")

        return None

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            None,
            0,
            None,
        )

        raise SyntaxError(message, syntaxErrorArgs)


class Node:
    def __init__(self, type, children: list):
        self.type = type
        self.children = children
