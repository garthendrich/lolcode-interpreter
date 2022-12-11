from copy import deepcopy
from .abstractions import ABSTRACTION
from .token_enum import TOKEN
from .utils import isEmpty, toNumber
import easygui


class Parser:
    def parse(self, sourceCode, lexemes):
        self.currentLineNumber = 1
        self.sourceCodeLines = sourceCode.split("\n")
        self.lexemes = lexemes

        self.memory = {}
        self.memoryStack = []
        self.outputBuffer = ""

        self.canGTFO = False

        return self._Program()

    def _nextTokenIs(self, tokenType):
        if isEmpty(self.lexemes):
            return

        return self.lexemes[0].lexemeType == tokenType

    def _popNext(self):
        self._updateCurrentLineNumber()

        if isEmpty(self.lexemes):
            return

        return self.lexemes.pop(0)

    def _updateCurrentLineNumber(self):
        if self._nextTokenIs(TOKEN.LINEBREAK):
            self.currentLineNumber += 1

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

    def _enterNewScope(self):
        self.memoryStack.append(deepcopy(self.memory))

    def _exitCurrentScope(self):
        self.memory = self.memoryStack.pop()

    def _throwError(self, errorType, message):
        errorArgs = (
            None,
            self.currentLineNumber,
            0,  # not yet implemented
            self.sourceCodeLines[self.currentLineNumber - 1],
        )

        raise errorType(message, errorArgs)

    def _Program(self):

        while self._nextTokenIs(TOKEN.LINEBREAK):
            self._popNext()

        self._expectNext(TOKEN.CODE_DELIMITER, 'Missing starting keyword "HAI"')

        self._expectNext(TOKEN.LINEBREAK, "Missing linebreak")
        while self._nextTokenIs(TOKEN.LINEBREAK):
            self._popNext()

        self._Statements()

        self._expectNext(TOKEN.CODE_DELIMITER, 'Missing ending keyword "KTHXBYE"')

    def _Statements(self):
        statement = (
            self._Declaration()
            or self._Output()
            or self._RecastingStatement()
            or self._AssignmentStatement()
            or self._LoopStatement()
            or self._Input()
            or self._IfStatement()
            or self._CaseStatement()
            or self._BreakStatement()
        )

        if statement is None:
            statement = self._Operand()
            if statement is not None:
                self._assign(TOKEN.IT_VARIABLE, statement)

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
        if self._nextTokenIs(TOKEN.OUTPUT_KEYWORD):
            self._popNext()

            value = self._Operand()
            if value is None:
                self._throwError(SyntaxError, "Expected an operand")

            self._output(value)

            while not self._nextTokenIs(TOKEN.LINEBREAK):
                if self._nextTokenIs(TOKEN.OPERAND_SEPARATOR):
                    self._popNext()

                value = self._Operand()
                if value is None:
                    self._throwError(SyntaxError, "Expected an operand")

                self._output(value)

            self._output("\n")

            return True

        return None

    def _output(self, value):
        if isinstance(value, bool):
            value = "WIN" if value == True else "FAIL"

        self.outputBuffer += str(value)

    def _Input(self):
        children = []

        if self._nextTokenIs(TOKEN.INPUT_KEYWORD):
            self._popNext()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNext()
                variableIdentifier = variableIdentifierToken.lexeme

                value = easygui.enterbox(self.outputBuffer)
                self._assign(variableIdentifier, value)

                return True

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

        explicitTypecast = self._ExplicitTypecast()
        if explicitTypecast is not None:
            return explicitTypecast

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

    def _operate(self, operationToken, a, b):
        if operationToken.lexemeType == TOKEN.ADDITION_OPERATION:
            return toNumber(a) + toNumber(b)
        if operationToken.lexemeType == TOKEN.SUBTRACTION_OPERATION:
            return toNumber(a) - toNumber(b)
        if operationToken.lexemeType == TOKEN.MULTIPLICATION_OPERATION:
            return toNumber(a) * toNumber(b)
        if operationToken.lexemeType == TOKEN.QUOTIENT_OPERATION:
            return toNumber(a) / toNumber(b)
        if operationToken.lexemeType == TOKEN.MODULO_OPERATION:
            return toNumber(a) % toNumber(b)
        if operationToken.lexemeType == TOKEN.MAX_OPERATION:
            return max(toNumber(a), toNumber(b))
        if operationToken.lexemeType == TOKEN.MIN_OPERATION:
            return min(toNumber(a), toNumber(b))
        if operationToken.lexemeType == TOKEN.AND_OPERATION:
            return bool(a) and bool(b)
        if operationToken.lexemeType == TOKEN.OR_OPERATION:
            return bool(a) or bool(b)
        if operationToken.lexemeType == TOKEN.XOR_OPERATION:
            return (bool(a) and not bool(b)) or (not bool(a) and bool(b))
        if operationToken.lexemeType == TOKEN.EQUAL_TO_OPERATION:
            return toNumber(a) == toNumber(b)
        if operationToken.lexemeType == TOKEN.NOT_EQUAL_TO_OPERATION:
            return toNumber(a) != toNumber(b)

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
            or self._nextTokenIs(TOKEN.EQUAL_TO_OPERATION) 
            or self._nextTokenIs(TOKEN.NOT_EQUAL_TO_OPERATION)
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

        if (
            self._nextTokenIs(TOKEN.INFINITE_ARITY_AND_OPERATION)
            or self._nextTokenIs(TOKEN.INFINITE_ARITY_OR_OPERATION)
            or self._nextTokenIs(TOKEN.CONCATENATION_OPERATION)
        ):
            operationToken = self._popNext()

            if operationToken.lexemeType == TOKEN.CONCATENATION_OPERATION:
                needsMkay = False
            else:
                needsMkay = True

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

                    if needsMkay:
                        self._expectNext(
                            TOKEN.INFINITE_ARITY_DELIMITER, 'Missing keyword "MKAY"'
                        )

                    if operationToken.lexemeType == TOKEN.INFINITE_ARITY_AND_OPERATION:
                        return all(operandValues)
                    if operationToken.lexemeType == TOKEN.INFINITE_ARITY_OR_OPERATION:
                        return any(operandValues)
                    if operationToken.lexemeType == TOKEN.CONCATENATION_OPERATION:
                        return "".join(operandValues)

                self._throwError(SyntaxError, "Expected an operand")

            self._throwError(SyntaxError, "Expected an operand")

        return None

    def _typeCast(self, type, value):
        if type == "TROOF":
            return bool(value)

        if type == "NUMBAR":
            return float(value) if value != None else 0.0

        if type == "NUMBR":
            return int(value) if value != None else 0

        if type == "YARN":
            if value == None:
                return ""

            if isinstance(value, bool):
                return "WIN" if value else "FAIL"

            if isinstance(value, int) or isinstance(value, float):
                return str(round(value, 2))

    def _ExplicitTypecast(self):
        if self._nextTokenIs(TOKEN.EXPLICIT_TYPECASTING_KEYWORD):
            self._popNext()

            if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                variableIdentifierToken = self._popNext()
                variableIdentifier = variableIdentifierToken.lexeme
                value = self._getValue(variableIdentifier)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    typeToken = self._popNext()

                    return self._typeCast(typeToken.lexeme, value)

                self._throwError(SyntaxError, "Expected a type")

            self._throwError(SyntaxError, "Expected a variable")

        return None

    def _AssignmentStatement(self):

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            variableIdentifierToken = self._popNext()
            variableIdentifier = variableIdentifierToken.lexeme
            value = None

            if self._nextTokenIs(TOKEN.VARIABLE_ASSIGNMENT):
                print("assigning var")
                self._popNext()

                value = self._Operand()
                if value is None:
                    self._throwError(SyntaxError, "Expected operand")

                self._assign(variableIdentifier, value)

                return True

            self.lexemes.insert(0, variableIdentifierToken)

            return None

        return None

    def _RecastingStatement(self):

        if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
            variableIdentifierToken = self._popNext()
            variableIdentifier = variableIdentifierToken.lexeme
            value = None

            if self._nextTokenIs(TOKEN.RECASTING_KEYWORD):
                print("recasting var")
                self._popNext()

                value = self._getValue(variableIdentifier)

                if self._nextTokenIs(TOKEN.TYPE_LITERAL):
                    typeToken = self._popNext()

                    typedValue = self._typeCast(typeToken.lexeme, value)

                    self._assign(variableIdentifier, typedValue)

                    return True

                self._throwError(SyntaxError, "Expected operand")

            self.lexemes.insert(0, variableIdentifierToken)

            return None

        return None

    def _IfStatement(self):

        if self._nextTokenIs(TOKEN.IF_ELSE_DELIMITER):
            self._popNext()

            statementBlockDict = {}

            self._expectNext(TOKEN.LINEBREAK, "Expected a linebreak")
            self._expectNext(TOKEN.IF_STATEMENT_KEYWORD, "Expected 'YA RLY'")
            self._expectNext(TOKEN.LINEBREAK, "Expected a linebreak")

            while self._nextTokenIs(TOKEN.LINEBREAK):
                self._popNext()

            ifBlockLexemes = []
            while not (
                self._nextTokenIs(TOKEN.ELSE_STATEMENT_KEYWORD)
                or self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
            ):
                ifBlockLexemes.append(self._popNext())

            statementBlockDict[self._getValue(TOKEN.IT_VARIABLE)] = ifBlockLexemes

            if self._nextTokenIs(TOKEN.ELSE_STATEMENT_KEYWORD):
                self._popNext()

                self._expectNext(TOKEN.LINEBREAK, "Expected a linebreak")

                while self._nextTokenIs(TOKEN.LINEBREAK):
                    self._popNext()

                elseBlockLexemes = []
                while not self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER):
                    elseBlockLexemes.append(self._popNext())

                if True not in statementBlockDict.keys():
                    statementBlockDict[True] = elseBlockLexemes

            self._expectNext(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER, "Expected 'OIC'")

            if True in statementBlockDict.keys():
                remainingLexemes = self.lexemes

                currentLineNumber = self.currentLineNumber
                self.lexemes = statementBlockDict[True]
                self.currentLineNumber = 0

                self._enterNewScope()
                self._Statements()
                self._exitCurrentScope()

                self.lexemes = remainingLexemes
                self.currentLineNumber = currentLineNumber

            return True

        return None

    def _BreakStatement(self):

        if self.canGTFO:

            if self._nextTokenIs(TOKEN.BREAK_STATEMENT):

                self.lexemes = []
                return None

        return None

    def _CaseStatement(self):

        if self._nextTokenIs(TOKEN.SWITCH_CASE_STATEMENT_DELIMITER):
            self._popNext()

            statementBlockLocation = {}
            caseCodeBlock = []
            it_var = self._getValue(TOKEN.IT_VARIABLE)

            self._expectNext(TOKEN.LINEBREAK, "Expected a linebreak")
            self._expectNext(TOKEN.CASE_KEYWORD, "Expected keyword 'OMG'")

            operand = self._Operand()
            if operand is not None:

                self._expectNext(TOKEN.LINEBREAK, "Expected a linebreak")

                while self._nextTokenIs(TOKEN.LINEBREAK):
                    self._popNext()

                statementBlockLocation[str(operand)] = 0

                while not (
                    self._nextTokenIs(TOKEN.CASE_KEYWORD)
                    or self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD)
                    or self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
                ):
                    caseCodeBlock.append(self._popNext())

                while True:
                    if self._nextTokenIs(TOKEN.CASE_KEYWORD):
                        self._popNext()

                        operand = self._Operand()
                        if operand is not None:

                            while self._nextTokenIs(TOKEN.LINEBREAK):
                                self._popNext()

                            if str(it_var) not in statementBlockLocation.keys():
                                statementBlockLocation[str(operand)] = len(
                                    caseCodeBlock
                                )

                            while not (
                                self._nextTokenIs(TOKEN.CASE_KEYWORD)
                                or self._nextTokenIs(
                                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER
                                )
                                or self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD)
                            ):
                                caseCodeBlock.append(self._popNext())

                        else:
                            self._throwError(SyntaxError, "Missing Operand")
                    else:
                        break

                if self._nextTokenIs(TOKEN.DEFAULT_CASE_KEYWORD):
                    self._popNext()

                    while self._nextTokenIs(TOKEN.LINEBREAK):
                        self._popNext()

                    if str(it_var) not in statementBlockLocation.keys():
                        statementBlockLocation[str(it_var)] = len(caseCodeBlock)

                    while not (
                        self._nextTokenIs(TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER)
                    ):
                        caseCodeBlock.append(self._popNext())

                self._expectNext(
                    TOKEN.FLOW_CONTROL_STATEMENTS_DELIMITER, "Expected 'OIC'"
                )

                if str(it_var) in statementBlockLocation.keys():

                    currentLineNumber = self.currentLineNumber
                    remainingLexemes = self.lexemes
                    self.canGTFO = True

                    self.lexemes = caseCodeBlock[
                        statementBlockLocation[it_var] : len(caseCodeBlock)
                    ]

                    self.currentLineNumber = 0

                    self._enterNewScope()
                    self._Statements()
                    self._exitCurrentScope()

                    self.lexemes = remainingLexemes
                    self.currentLineNumber = currentLineNumber

                return True

            self._throwError(SyntaxError, "Missing Operand")

        return None

    # !!! no nested loops
    # !!! does not verify loop identifier
    def _LoopStatement(self):
        if self._nextTokenIs(TOKEN.LOOP_DECLARATION_AND_DELIMITER):
            self._popNext()

            loopHeaderLineNumber = self.currentLineNumber

            if self._nextTokenIs(TOKEN.LOOP_IDENTIFIER):
                loopIdentifierToken = self._popNext()
                loopIdentifier = loopIdentifierToken.lexeme

                if self._nextTokenIs(TOKEN.INCREMENT_KEYWORD) or self._nextTokenIs(
                    TOKEN.DECREMENT_KEYWORD
                ):
                    deltaToken = self._popNext()
                    if deltaToken.lexeme == "UPPIN":
                        delta = 1
                    elif deltaToken.lexeme == "NERFIN":
                        delta = -1

                    self._expectNext(TOKEN.KEYWORD_IN_LOOP, 'Missing keyword "YR"')

                    if self._nextTokenIs(TOKEN.VARIABLE_IDENTIFIER):
                        variableIdentifierToken = self._popNext()
                        variableIdentifier = variableIdentifierToken.lexeme

                        conditionExpressionLexemes = []
                        hasLoopCondition = False
                        if self._nextTokenIs(TOKEN.LOOP_CONDITION_KEYWORD):
                            loopConditionKeywordToken = self._popNext()

                            hasLoopCondition = True

                            while not self._nextTokenIs(TOKEN.LINEBREAK):
                                conditionExpressionLexemes.append(self._popNext())

                        self._expectNext(
                            TOKEN.LINEBREAK, "Missing condition or new line"
                        )

                        while self._nextTokenIs(TOKEN.LINEBREAK):
                            self._popNext()

                        loopBlockLexemes = []
                        while not self._nextTokenIs(TOKEN.LOOP_DELIMITER):
                            loopBlockLexemes.append(self._popNext())

                        self._expectNext(TOKEN.LOOP_DELIMITER, "Missing loop closing")

                        self._expectNext(
                            TOKEN.LOOP_IDENTIFIER, "Missing loop identifier"
                        )

                        remainderLexemes = self.lexemes

                        while True:
                            self.lexemes = conditionExpressionLexemes + loopBlockLexemes
                            self.currentLineNumber = loopHeaderLineNumber + 1

                            if hasLoopCondition:
                                if loopConditionKeywordToken.lexeme == "WILE":
                                    loopRunCondition = self._Operand()
                                elif loopConditionKeywordToken.lexeme == "TIL":
                                    loopRunCondition = not self._Operand()

                                if not loopRunCondition:
                                    break

                            self._enterNewScope()
                            self._Statements()
                            self._exitCurrentScope()

                            self._assign(
                                variableIdentifier,
                                self._getValue(variableIdentifier) + delta,
                            )

                        self.lexemes = remainderLexemes

                        return True

                    self._throwError(SyntaxError, "Missing variable")

                self._throwError(SyntaxError, "Missing UPPIN/NERFIN keyword")

            self._throwError(SyntaxError, "Missing loop name")

        return None
