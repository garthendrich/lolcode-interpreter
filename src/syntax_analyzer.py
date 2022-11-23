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
        self.lexemes.pop(0)

        statements = self._Statements()

        if len(statements.body) == 0:
            self._throwSyntaxError("Expected statements")

        if self._lookahead().lexemeType is not TOKEN.CODE_DELIMITER:
            self._throwSyntaxError('Missing ending keyword "KTHXBYE"')

        return Node(ABSTRACTION.PROGRAM, statements)

    def _Statements(self):
        statements = []

        declaration = self._Declaration()
        if declaration is not None:
            statements.append(declaration)

        output = self._Output()
        if output is not None:
            statements.append(output)

        addition = self._Addition()
        if addition is not None:
            statements.append(addition)

        subtraction = self._Subtraction()
        if subtraction is not None:
            statements.append(subtraction)

        multiplication = self._Multiplication()
        if multiplication is not None:
            statements.append(multiplication)

        division = self._Division()
        if division is not None:
            statements.append(division)

        max = self._Max()
        if max is not None:
            statements.append(max)

        min = self._Min()
        if min is not None:
            statements.append(min)

        if len(statements) == 0:
            self._throwSyntaxError("Statement error")

        if self._lookahead().lexemeType is TOKEN.LINEBREAK:
            self.lexemes.pop(0)
            if self._lookahead().lexemeType is not TOKEN.CODE_DELIMITER:
                statements.append(self._Statements())

        return Node(ABSTRACTION.STATEMENT, statements)

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
            return Node(lexeme.lexemeType, lexeme.lexeme)
        
        if self._lookahead().lexemeType is TOKEN.FLOAT_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.INTEGER_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.STRING_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.TYPE_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        if self._lookahead().lexemeType is TOKEN.STRING_LITERAL:
            lexeme = self.lexemes.pop(0)
            return Node(lexeme.lexemeType, lexeme.lexeme)

        return

    def _Addition(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.ADDITION_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.SUM, body)

    def _Subtraction(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.SUBTRACTION_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.DIFF, body)

    def _Multiplication(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.MULTIPLICATION_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.MUL, body)

    def _Division(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.QUOTIENT_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.DIV, body)

    def _Max(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.MAX_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.MAX, body)

    def _Min(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.MIN_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.MIN, body)

    def _And(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.AND_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.AND, body)

    def _Or(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.OR_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.OR, body)

    def _Xor(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.XOR_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)
        
        if self._lookahead().lexemeType is not TOKEN.OPERAND_SEPARATOR:
            return
        body.append(self.lexemes.pop(0))

        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.XOR, body)

    def _Not(self):
        body = []

        if self._lookahead().lexemeType is not TOKEN.NOT_OPERATION:
            return
        body.append(self.lexemes.pop(0))
        
        operand = self._Operand()
        if operand is not None:
            body.append(operand)

        return Node(ABSTRACTION.NOT, body)

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
    def __init__(self, type, body):
        self.type = type
        self.body = body
