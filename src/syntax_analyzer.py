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
        return list.append(self._popNext())

    def _Program(self):
        children = []

        if not self._nextTokenIs(TOKEN.CODE_DELIMITER):
            self._throwSyntaxError('Missing starting keyword "HAI"')
        self._moveNextTokenTo(children)

        if not self._nextTokenIs(TOKEN.LINEBREAK):
            self._throwSyntaxError("Unexpected keyword")
        self._moveNextTokenTo(children)

        children.append(self._Statements())

        # if not self._nextTokenIs(TOKEN.LINEBREAK):
        #     self._throwSyntaxError("Unexpected keyword")
        # self._moveNextTokenTo(programChildren)

        if not self._nextTokenIs(TOKEN.CODE_DELIMITER):
            self._throwSyntaxError('Missing starting keyword "KTHXBYE"')
        self._moveNextTokenTo(children)

        return Node(ABSTRACTION.PROGRAM, children)

    def _Statements(self):
        children = []

        declaration = self._Declaration()
        if declaration is not None:
            children.append(declaration)

        output = self._Output()
        if output is not None:
            children.append(output)

        addition = self._Addition()
        if addition is not None:
            children.append(addition)

        subtraction = self._Subtraction()
        if subtraction is not None:
            children.append(subtraction)

        multiplication = self._Multiplication()
        if multiplication is not None:
            children.append(multiplication)

        division = self._Division()
        if division is not None:
            children.append(division)

        max = self._Max()
        if max is not None:
            children.append(max)

        min = self._Min()
        if min is not None:
            children.append(min)

        if len(children) == 0:
            self._throwSyntaxError("Statement error")

        if self._nextTokenIs(TOKEN.LINEBREAK):
            self.lexemes.pop(0)
            if not self._nextTokenIs(TOKEN.CODE_DELIMITER):
                children.append(self._Statements())

        return Node(ABSTRACTION.STATEMENT, children)

    def _Declaration(self):
        children = []

        if not self._nextTokenIs(TOKEN.VARIABLE_DECLARATION):
            return
        self._moveNextTokenTo(children)

        if not self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            return
        self._moveNextTokenTo(children)

        if not self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
            return Node(ABSTRACTION.DECLARATION, children)
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is None:
            self._throwSyntaxError("Needs value")
        children.append(operand)

        return Node(ABSTRACTION.DECLARATION, children)

    def _Output(self):
        children = []

        if not self._nextTokenIs(TOKEN.OUTPUT_KEYWORD):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is None:
            return
        children.append(operand)

        return Node(ABSTRACTION.OUTPUT, children)

    def _Operand(self):
        literal = self._Literal()
        if literal is not None:
            return Node(ABSTRACTION.OUTPUT, literal)

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        return

    def _Literal(self):
        if self._nextTokenIs(TOKEN.BOOL_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._nextTokenIs(TOKEN.FLOAT_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._nextTokenIs(TOKEN.INTEGER_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._nextTokenIs(TOKEN.STRING_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        if self._nextTokenIs(TOKEN.TYPE_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._nextTokenIs(TOKEN.STRING_LITERAL):
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        return

    def _Addition(self):
        children = []

        if not self._nextTokenIs(TOKEN.ADDITION_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.SUM, children)

    def _Subtraction(self):
        children = []

        if not self._nextTokenIs(TOKEN.SUBTRACTION_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.DIFF, children)

    def _Multiplication(self):
        children = []

        if not self._nextTokenIs(TOKEN.MULTIPLICATION_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.MUL, children)

    def _Division(self):
        children = []

        if not self._nextTokenIs(TOKEN.QUOTIENT_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.DIV, children)

    def _Max(self):
        children = []

        if not self._nextTokenIs(TOKEN.MAX_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.MAX, children)

    def _Min(self):
        children = []

        if not self._nextTokenIs(TOKEN.MIN_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.MIN, children)

    def _And(self):
        children = []

        if not self._nextTokenIs(TOKEN.AND_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.AND, children)

    def _Or(self):
        children = []

        if not self._nextTokenIs(TOKEN.OR_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.OR, children)

    def _Xor(self):
        children = []

        if not self._nextTokenIs(TOKEN.XOR_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        if not self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.XOR, children)

    def _Not(self):
        children = []

        if not self._nextTokenIs(TOKEN.NOT_OPERATION):
            return
        self._moveNextTokenTo(children)

        operand = self._Operand()
        if operand is not None:
            children.append(operand)

        return Node(ABSTRACTION.NOT, children)

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            None,
            0,
            None,
        )

        print(message)

        # raise SyntaxError(message, syntaxErrorArgs)


class Node:
    def __init__(self, type, children: list):
        self.type = type
        self.children = children
