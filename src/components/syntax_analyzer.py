from .abstractions import ABSTRACTION
from .token_enum import TOKEN
from .utils import isEmpty


class Parser:
    def _nextTokenIs(self, tokenType):
        self._catchEndOfLine()
        return self.lexemes[0].lexemeType == tokenType

    def _popNext(self):
        self._catchEndOfLine()
        return self.lexemes.pop(0)

    def _catchEndOfLine(self):
        if isEmpty(self.lexemes):
            self._throwSyntaxError("Unexpected end of line")

    def _expectNext(self, tokenType, errorMessage):
        if self._nextTokenIs(tokenType):
            self._popNext()
        else:
            self._throwSyntaxError(errorMessage)

    def _assign(self, identifier, value):
        self.memory[identifier] = value

    # remove after reimplementation
    def _moveNextTokenTo(self, list):
        list.append(self._popNext())

    def parse(self, lexemes):
        self.lexemes = lexemes

        self.memory = {}

        return self._Program()

    def _Program(self):
        self._expectNext(TOKEN.CODE_DELIMITER, 'Missing starting keyword "HAI"')

        self._expectNext(TOKEN.LINEBREAK, "Missing linebreak")
        while self._nextTokenIs(TOKEN.LINEBREAK):
            self._popNext()

        self._Statements()

        self._expectNext(TOKEN.CODE_DELIMITER, 'Missing starting keyword "KTHXBYE"')

    def _Statements(self):
        statement = (
            self._Declaration()
            or self._Output()
            or self._TwoOperandOperation()
            or self._MultipleOperandOperation()
            or self._ConcatOperation()
            or self._ComparisonOperation()
            or self._ExplicitTypecast()
            or self._RecastingAndAssignment()
            or self._IfStatement()
            or self._CaseStatement()
            or self._LoopStatement()
            or self._Input()
        )

        if statement is not None:
            self._expectNext(TOKEN.LINEBREAK, "Expected linebreak")
            while self._nextTokenIs(TOKEN.LINEBREAK):
                self._popNext()

            self._Statements()

    def _Declaration(self):
        if self._nextTokenIs(TOKEN.VARIABLE_DECLARATION):
            self._popNext()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNext()
                variableIdentifier = variableIdentifierToken.lexeme
                value = None

                if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                    self._popNext()

                    value = self._Operand()
                    if value is None:
                        self._throwSyntaxError("Expected an expression")

                self._assign(variableIdentifier, value)
                return True

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

            while not self._nextTokenIs(TOKEN.LINEBREAK):
                operand = self._Operand()
                if operand is None:
                    self._throwSyntaxError("Expected an operand")

                children.append(operand)

            return Node(ABSTRACTION.OUTPUT, children)

        return None

    def _Input(self):
        children = []

        if self._nextTokenIs(TOKEN.INPUT_KEYWORD):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                self._moveNextTokenTo(children)

                return Node(ABSTRACTION.INPUT, children)

        return None

    def _Operand(self):
        literalValue = self._Literal()
        print(literalValue, type(literalValue))
        if literalValue is not None:
            return literalValue

        # !!! ---

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            lexeme = self._popNext()
            return Node(ABSTRACTION.OPERAND, lexeme.lexeme)

        operationOperand = (
            self._TwoOperandOperation()
            or self._OneOperandOperation()
            or self._MultipleOperandOperation()
            or self._ComparisonOperation()
            or self._ConcatOperation()
            or self._ExplicitTypecast()
        )
        if operationOperand is not None:
            return Node(ABSTRACTION.OPERAND, operationOperand)

        return None

    def _Literal(self):
        if self._nextTokenIs(TOKEN.BOOL_LITERAL):
            boolToken = self._popNext()
            return True if boolToken.lexeme == "WIN" else False

        if self._nextTokenIs(TOKEN.FLOAT_LITERAL):
            integerToken = self._popNext()
            return float(integerToken.lexeme)

        if self._nextTokenIs(TOKEN.INTEGER_LITERAL):
            integerToken = self._popNext()
            return int(integerToken.lexeme)

        if self._nextTokenIs(TOKEN.STRING_LITERAL):
            stringToken = self._popNext()

            return stringToken.lexeme[1:-1]  # remove quotes

        if self._nextTokenIs(TOKEN.TYPE_LITERAL):
            typeToken = self._popNext()
            return typeToken.lexeme  # ?????

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

    def _OneOperandOperation(self):
        children = []

        if self._nextTokenIs(TOKEN.NOT_OPERATION):
            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is not None:
                children.append(operand)

                return Node("operation", children)

            self._throwSyntaxError("Expected an operand")

        return None

    def _MultipleOperandOperation(self):
        children = []

        if self._nextTokenIs(TOKEN.INFINITE_ARITY_AND_OPERATION) or self._nextTokenIs(
            TOKEN.INFINITE_ARITY_OR_OPERATION
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

                        while True:
                            if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                                self._moveNextTokenTo(children)

                                operand = self._Operand()
                                if operand is not None:
                                    children.append(operand)

                                else:
                                    self._throwSyntaxError("Expected an operand")

                            else:
                                break

                        if self._nextTokenIs(TOKEN.INFINITE_ARITY_DELIMITER):
                            self._moveNextTokenTo(children)

                            return Node("multiple operand operation", children)

                        self._throwSyntaxError('Missing keyword "Mkay"')

                    self._throwSyntaxError("Expected an operand")

                self._throwSyntaxError('Missing keyword "AN"')

            self._throwSyntaxError("Expected an operand")

        return None

    def _ConcatOperation(self):
        children = []

        if self._nextTokenIs(TOKEN.CONCATENATION_OPERATION):

            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is not None:
                children.append(operand)

                if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                    self._moveNextTokenTo(children)

                    operand = self._Operand()
                    if operand is not None:
                        children.append(operand)

                        while True:
                            if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                                self._moveNextTokenTo(children)

                                operand = self._Operand()
                                if operand is not None:
                                    children.append(operand)

                                else:
                                    self._throwSyntaxError("Expected an operand")

                            else:
                                break

                        return Node("concatenation operation", children)

                    self._throwSyntaxError("Expected an operand")

                self._throwSyntaxError('Missing keyword "AN"')

            self._throwSyntaxError("Expected an operand")

        return None

    def _ComparisonOperation(self):
        children = []

        if self._nextTokenIs(TOKEN.EQUAL_TO_OPERATION) or self._nextTokenIs(
            TOKEN.NOT_EQUAL_TO_OPERATION
        ):
            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is not None:
                children.append(operand)

                if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                    self._moveNextTokenTo(children)

                    if self._nextTokenIs(TOKEN.MAX_OPERATION) or self._nextTokenIs(
                        TOKEN.MIN_OPERATION
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

                            return Node("comparison operation", children)

                    operand = self._Operand()
                    if operand is not None:
                        children.append(operand)

                        return Node("comparison operation", children)

                    self._throwSyntaxError("Expected an operand")

                self._throwSyntaxError('Missing keyword "AN"')

            self._throwSyntaxError("Expected an operand")

        return None

    def _ExplicitTypecast(self):
        children = []

        if self._nextTokenIs(TOKEN.EXPLICIT_TYPECASTING_KEYWORD):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    self._moveNextTokenTo(children)

                    return Node("explicit typecast operation", children)

                self._throwSyntaxError("Expected a type literal")

            self._throwSyntaxError("Expected a variable identifier")

        return None

    def _RecastingAndAssignment(self):
        children = []

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                self._moveNextTokenTo(children)

                operand = self._Operand()
                recastTypecast = self._ExplicitTypecast()
                if operand is not None:
                    children.append(operand)

                    return Node("assignment statement", children)

                elif recastTypecast is not None:
                    children.append(recastTypecast)

                    return Node("recast typecast", children)

                else:
                    self._throwSyntaxError("Expected operand")

            elif self._nextTokenIs(TOKEN.RECASTING_KEYWORD):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    self._moveNextTokenTo(children)

                    return Node("recast typecast", children)

                self._throwSyntaxError("Expected operand")

            self._throwSyntaxError("Expected assignment keyword")

        return None

    def _IfStatement(self):
        children = []

        if self._nextTokenIs(TOKEN.IF_ELSE_DELIMITER):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.LINEBREAK):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.IF_STATEMENT_KEYWORD):
                    self._moveNextTokenTo(children)

                    if self._nextTokenIs(TOKEN.LINEBREAK):
                        self._moveNextTokenTo(children)

                        statement = self._Statements()
                        if statement is not None:
                            children.append(statement)

                            if self._nextTokenIs(TOKEN.ELSE_STATEMENT_KEYWORD):
                                self._moveNextTokenTo(children)

                                if self._nextTokenIs(TOKEN.LINEBREAK):
                                    self._moveNextTokenTo(children)

                                    statement = self._Statements()
                                    if statement is not None:
                                        children.append(statement)

                                    else:
                                        self._throwSyntaxError("Missing statement")

                                else:
                                    self._throwSyntaxError("Missing linebreak")

                            if self._nextTokenIs(
                                TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                            ):
                                self._moveNextTokenTo(children)

                                return Node("if statement operation", children)

                            self._throwSyntaxError('Missing keyword "OIC"')

                        self._throwSyntaxError("Missing statement")

                    self._throwSyntaxError("Missing linebreak")

                self._throwSyntaxError('Missing keyword "O RLY"')

            self._throwSyntaxError("Missing linebreak")

        return None

    def _CaseStatement(self):
        children = []

        if self._nextTokenIs(TOKEN.SWITCH_CASE_STATEMENT_DELIMITER):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.LINEBREAK):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.CASE_KEYWORD):
                    self._moveNextTokenTo(children)

                    operand = self._Operand()
                    if operand is not None:
                        children.append(operand)

                        if self._nextTokenIs(TOKEN.LINEBREAK):
                            self._moveNextTokenTo(children)

                            statement = self._Statements()
                            if statement is not None:
                                children.append(statement)

                                while True:
                                    if self._nextTokenIs(TOKEN.CASE_KEYWORD):
                                        self._moveNextTokenTo(children)

                                        operand = self._Operand()
                                        if operand is not None:
                                            children.append(operand)

                                            if self._nextTokenIs(TOKEN.LINEBREAK):
                                                self._moveNextTokenTo(children)

                                                statement = self._Statements()
                                                if statement is not None:
                                                    children.append(statement)

                                                else:
                                                    self._throwSyntaxError(
                                                        "Missing statement"
                                                    )

                                            else:
                                                self._throwSyntaxError(
                                                    "Missing linebreak"
                                                )

                                    else:
                                        break

                                if self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD):
                                    self._moveNextTokenTo(children)

                                    if self._nextTokenIs(TOKEN.LINEBREAK):
                                        self._moveNextTokenTo(children)

                                        statement = self._Statements()
                                        if statement is not None:
                                            children.append(statement)

                                        else:
                                            self._throwSyntaxError("Missing statement")

                                    else:
                                        self._throwSyntaxError("Missing linebreak")

                                if self._nextTokenIs(
                                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                                ):
                                    self._moveNextTokenTo(children)

                                    return Node("case statement operation", children)

                                self._throwSyntaxError('Missing keyword "OIC"')

                            self._throwSyntaxError("Missing statement")

                        self._throwSyntaxError("Missing linebreak")

                    self._throwSyntaxError("Missing Operand")

                self._throwSyntaxError('Missing keyword "O RLY"')

            self._throwSyntaxError("Missing linebreak")

        return None

    def _LoopStatement(self):
        children = []

        if self._nextTokenIs(TOKEN.LOOP_DECLARATION_AND_DELIMITER):
            self._moveNextTokenTo(children)

            if self._nextTokenIs(TOKEN.LOOP_IDENTIFIER):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.INCREMENT_KEYWORD) or self._nextTokenIs(
                    TOKEN.DECREMENT_KEYWORD
                ):
                    self._moveNextTokenTo(children)

                    if self._nextTokenIs(TOKEN.KEYWORD_IN_LOOP):
                        self._moveNextTokenTo(children)

                        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                            self._moveNextTokenTo(children)

                            if self._nextTokenIs(TOKEN.LOOP_CONDITION_KEYWORD):
                                self._moveNextTokenTo(children)

                                troofExpression = (
                                    self._ComparisonOperation()
                                    or self._TwoOperandOperation()
                                    or self._MultipleOperandOperation()
                                )
                                if troofExpression is not None:
                                    children.append(troofExpression)

                                else:
                                    self._throwSyntaxError("Missing Troof Expression")

                            if self._nextTokenIs(TOKEN.LINEBREAK):
                                self._moveNextTokenTo(children)

                                statement = self._Statements()
                                if statement is not None:
                                    children.append(statement)

                                if self._nextTokenIs(TOKEN.LOOP_DELIMITER):
                                    self._moveNextTokenTo(children)

                                    if self._nextTokenIs(TOKEN.LOOP_IDENTIFIER):
                                        self._moveNextTokenTo(children)

                                        return Node("loop statement", children)

                                    self._throwSyntaxError("Missing Loop Identifier")

                                self._throwSyntaxError("Missing Loop Delimeter")

                            self._throwSyntaxError("Missing linebreak")

                        self._throwSyntaxError("Missing Variable Identifier")

                    self._throwSyntaxError('Missing keyword "YR"')

                self._throwSyntaxError("Missing UPPIN/NERFIN keyword")

            self._throwSyntaxError("Missing loop identifier")

        return None

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            None,
            0,
            None,
        )

        raise SyntaxError(message, syntaxErrorArgs)


# remove after reimplementation
class Node:
    def __init__(self, type, children: list):
        self.type = type
        self.children = children
