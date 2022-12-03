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
            self._throwError(SyntaxError, "Unexpected end of line")

    def _expectNext(self, tokenType, errorMessage):
        if self._nextTokenIs(tokenType):
            self._popNext()
        else:
            self._throwError(SyntaxError, errorMessage)

    def _assign(self, identifier, value):
        self.memory[identifier] = value

    def _getValue(self, identifier):
        if identifier in self.memory:
            return self.memory.get(identifier)

        self._throwError(NameError, f"{identifier} is not defined")

    # remove after reimplementation
    def _moveNextTokenTo(self, list):
        list.append(self._popNext())

    def _throwError(self, errorType, message):
        errorArgs = (
            None,
            None,
            0,
            None,
        )

        raise errorType(message, errorArgs)

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
                        self._throwError(SyntaxError, "Expected an expression")

                self._assign(variableIdentifier, value)
                return True

            self._throwError(SyntaxError, "Expected a variable identifier")

        return None

    def _Output(self):
        children = []

        if self._nextTokenIs(TOKEN.OUTPUT_KEYWORD):
            self._moveNextTokenTo(children)

            operand = self._Operand()
            if operand is None:
                self._throwError(SyntaxError, "Expected an operand")

            children.append(operand)

            while not self._nextTokenIs(TOKEN.LINEBREAK):
                operand = self._Operand()
                if operand is None:
                    self._throwError(SyntaxError, "Expected an operand")

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
        if literalValue is not None:
            return literalValue

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            identifierToken = self._popNext()
            return self._getValue(identifierToken.lexeme)

        operationValue = self._TwoOperandOperation()
        if operationValue is not None:
            return operationValue

        operationValue = self._NotOperation()
        if operationValue is not None:
            return operationValue

        operationValue = self._MultipleOperandOperation()
        if operationValue is not None:
            return operationValue

        # operationValue = self._ComparisonOperation()
        # if operationValue is not None:
        #     return operationValue

        # operationValue = self._ConcatOperation()
        # if operationValue is not None:
        #     return operationValue

        # operationValue = self._ExplicitTypecast()
        # if operationValue is not None:
        #     return operationValue

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
            return typeToken.lexeme  # !!! ?????

        return None

    # !!! no type checking
    def _operate(self, operationToken, a, b):
        if operationToken.lexemeType == TOKEN.ADDITION_OPERATION:
            return a + b
        elif operationToken.lexemeType == TOKEN.SUBTRACTION_OPERATION:
            return a - b
        elif operationToken.lexemeType == TOKEN.MULTIPLICATION_OPERATION:
            return a * b
        elif operationToken.lexemeType == TOKEN.QUOTIENT_OPERATION:
            return a / b
        elif operationToken.lexemeType == TOKEN.MODULO_OPERATION:
            return a % b
        elif operationToken.lexemeType == TOKEN.MAX_OPERATION:
            return max(a, b)
        elif operationToken.lexemeType == TOKEN.MIN_OPERATION:
            return min(a, b)
        elif operationToken.lexemeType == TOKEN.AND_OPERATION:
            return a and b
        elif operationToken.lexemeType == TOKEN.OR_OPERATION:
            return a or b
        elif operationToken.lexemeType == TOKEN.XOR_OPERATION:
            return (a and not b) or (not a and b)

    def _TwoOperandOperation(self):
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
            operationToken = self._popNext()

            firstOperandValue = self._Operand()
            if firstOperandValue is not None:
                self._expectNext(TOKEN.OPERAND_SEPARATOR, 'Missing keyword "AN"')

                secondOperandValue = self._Operand()
                if secondOperandValue is not None:
                    return self._operate(
                        operationToken, firstOperandValue, secondOperandValue
                    )

                self._throwError(SyntaxError, "Expected an operand")

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _NotOperation(self):
        if self._nextTokenIs(TOKEN.NOT_OPERATION):
            self._popNext()

            value = self._Operand()
            if value is not None:
                return not value

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _MultipleOperandOperation(self):
        operandValues = []

        if self._nextTokenIs(TOKEN.INFINITE_ARITY_AND_OPERATION) or self._nextTokenIs(
            TOKEN.INFINITE_ARITY_OR_OPERATION
        ):
            operationToken = self._popNext()

            firstOperandValue = self._Operand()
            if firstOperandValue is not None:
                operandValues.append(firstOperandValue)

                self._expectNext(TOKEN.OPERAND_SEPARATOR, 'Missing keyword "AN"')

                secondOperandValue = self._Operand()
                if secondOperandValue is not None:
                    operandValues.append(secondOperandValue)

                    while self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                        self._popNext()

                        operandValue = self._Operand()
                        if operandValue is not None:
                            operandValues.append(operandValue)
                        else:
                            self._throwError(SyntaxError, "Expected an operand")

                    self._expectNext(
                        TOKEN.INFINITE_ARITY_DELIMITER, 'Missing keyword "MKAY"'
                    )

                    if operationToken.lexemeType == TOKEN.INFINITE_ARITY_AND_OPERATION:
                        return all(operandValues)
                    elif operationToken.lexemeType == TOKEN.INFINITE_ARITY_OR_OPERATION:
                        return any(operandValues)

                self._throwError(SyntaxError, "Expected an operand")

            self._throwError(SyntaxError, "Expected an operand")

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
                                    self._throwError(SyntaxError, "Expected an operand")

                            else:
                                break

                        return Node("concatenation operation", children)

                    self._throwError(SyntaxError, "Expected an operand")

                self._throwError(SyntaxError, 'Missing keyword "AN"')

            self._throwError(SyntaxError, "Expected an operand")

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

                    self._throwError(SyntaxError, "Expected an operand")

                self._throwError(SyntaxError, 'Missing keyword "AN"')

            self._throwError(SyntaxError, "Expected an operand")

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

                self._throwError(SyntaxError, "Expected a type literal")

            self._throwError(SyntaxError, "Expected a variable identifier")

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
                    self._throwError(SyntaxError, "Expected operand")

            elif self._nextTokenIs(TOKEN.RECASTING_KEYWORD):
                self._moveNextTokenTo(children)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    self._moveNextTokenTo(children)

                    return Node("recast typecast", children)

                self._throwError(SyntaxError, "Expected operand")

            self._throwError(SyntaxError, "Expected assignment keyword")

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
                                        self._throwError(
                                            SyntaxError, "Missing statement"
                                        )

                                else:
                                    self._throwError(SyntaxError, "Missing linebreak")

                            if self._nextTokenIs(
                                TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                            ):
                                self._moveNextTokenTo(children)

                                return Node("if statement operation", children)

                            self._throwError(SyntaxError, 'Missing keyword "OIC"')

                        self._throwError(SyntaxError, "Missing statement")

                    self._throwError(SyntaxError, "Missing linebreak")

                self._throwError(SyntaxError, 'Missing keyword "O RLY"')

            self._throwError(SyntaxError, "Missing linebreak")

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
                                                    self._throwError(
                                                        SyntaxError, "Missing statement"
                                                    )

                                            else:
                                                self._throwError(
                                                    SyntaxError, "Missing linebreak"
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
                                            self._throwError(
                                                SyntaxError, "Missing statement"
                                            )

                                    else:
                                        self._throwError(
                                            SyntaxError, "Missing linebreak"
                                        )

                                if self._nextTokenIs(
                                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                                ):
                                    self._moveNextTokenTo(children)

                                    return Node("case statement operation", children)

                                self._throwError(SyntaxError, 'Missing keyword "OIC"')

                            self._throwError(SyntaxError, "Missing statement")

                        self._throwError(SyntaxError, "Missing linebreak")

                    self._throwError(SyntaxError, "Missing Operand")

                self._throwError(SyntaxError, 'Missing keyword "O RLY"')

            self._throwError(SyntaxError, "Missing linebreak")

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
                                    self._throwError(
                                        SyntaxError, "Missing Troof Expression"
                                    )

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

                                    self._throwError(
                                        SyntaxError, "Missing Loop Identifier"
                                    )

                                self._throwError(SyntaxError, "Missing Loop Delimeter")

                            self._throwError(SyntaxError, "Missing linebreak")

                        self._throwError(SyntaxError, "Missing Variable Identifier")

                    self._throwError(SyntaxError, 'Missing keyword "YR"')

                self._throwError(SyntaxError, "Missing UPPIN/NERFIN keyword")

            self._throwError(SyntaxError, "Missing loop identifier")

        return None


# remove after reimplementation
class Node:
    def __init__(self, type, children: list):
        self.type = type
        self.children = children
