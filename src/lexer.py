import re

from statement_enum import STATEMENT


class Lexer:
    def __init__(self):
        self.lexemes = []

        self.patternTypes = {
            r"^HAI$": STATEMENT.CODE_DELIMITER,
            r"^KTHXBYE$": STATEMENT.CODE_DELIMITER,
            r"^BTW$": STATEMENT.COMMENT_KEYWORD,
            r"^OBTW$": STATEMENT.MULTILINE_COMMENT_DELIMITER,
            r"^TLDR$": STATEMENT.MULTILINE_COMMENT_DELIMITER,
            r"^I HAS A$": STATEMENT.VARIABLE_DECLARATION,
            r"^ITZ$": STATEMENT.VARIABLE_ASSIGNMENT,
            r"^R$": STATEMENT.VARIABLE_ASSIGNMENT,
            r"^SUM OF$": STATEMENT.ADDITION_OPERATION,
            r"^DIFF OF$": STATEMENT.SUBTRACTION_OPERATION,
            r"^PRODUKT OF$": STATEMENT.MULTIPLICATION_OPERATION,
            r"^QUOSHUNT OF$": STATEMENT.QUOTIENT_OPERATION,
            r"^MOD OF$": STATEMENT.MODULO_OPERATION,
            r"^BIGGR OF$": STATEMENT.MAX_OPERATION,
            r"^SMALLR$": STATEMENT.MIN_OPERATION,
            r"^BOTH OF$": STATEMENT.AND_OPERATION,
            r"^EITHER OF$": STATEMENT.OR_OPERATION,
            r"^WON OF$": STATEMENT.XOR_OPERATION,
            r"^NOT$": STATEMENT.NOT_OPERATION,
            r"^ANY OF$": STATEMENT.INFINITE_ARITY_AND_OPERATION,
            r"^ALL OF$": STATEMENT.INFINITE_ARITY_OR_OPERATION,
            r"^BOTH SAEM$": STATEMENT.EQUAL_TO_OPERATION,
            r"^DIFFRINT$": STATEMENT.NOT_EQUAL_TO_OPERATION,
            r"^SMOOSH$": STATEMENT.CONCATENATION_OPERATION,
            r"^MAEK$": STATEMENT.EXPLICIT_TYPECASTING_KEYWORD,
            r"^A$": STATEMENT.OPTIONAL_A_KEYWORD,
            r"^AN$": STATEMENT.OPERAND_SEPARATOR,
            r"^MKAY$": STATEMENT.INFINITE_ARITY_DELIMITER,
            r"^IS NOW A$": STATEMENT.RECASTING_KEYWORD,
            r"^VISIBLE$": STATEMENT.OUTPUT_KEYWORD,
            r"^GIMMEH$": STATEMENT.INPUT_KEYWORD,
            r"^O RLY\?$": STATEMENT.IF_ELSE_DELIMITER,
            r"^YA RLY$": STATEMENT.IF_STATEMENT_KEYWORD,
            r"^MEBBE$": STATEMENT.ELSE_IF_STATEMENT_KEYWORD,
            r"^NO WAI$": STATEMENT.ELSE_STATEMENT_KEYWORD,
            r"^OIC$": STATEMENT.FLOW_CONTROL_STATEMENTS_DELIMITER,
            r"^WTF\?$": STATEMENT.SWITCH_CASE_STATEMENT_DELIMITER,
            r"^OMG$": STATEMENT.CASE_KEYWORD,
            r"^OMGTWF$": STATEMENT.DEFAULT_CASE_KEYWORD,
            r"^IM IN YR$": STATEMENT.LOOP_DECLARATION_AND_DELIMITER,
            r"^UPPIN$": STATEMENT.INCREMENT_KEYWORD,
            r"^NERFIN$": STATEMENT.DECREMENT_KEYWORD,
            r"^YR$": STATEMENT.KEYWORD_IN_LOOP,
            r"^TIL$": STATEMENT.LOOP_CONDITION_KEYWORD,
            r"^WILE$": STATEMENT.LOOP_CONDITION_KEYWORD,
            r"^IM OUTTA YR$": STATEMENT.LOOP_DELIMITER,
            r"^-?\d*.\d+$": STATEMENT.FLOAT_LITERAL,
            r"^-?\d+$": STATEMENT.INTEGER_LITERAL,
            r"^\".*\"$": STATEMENT.STRING_LITERAL,
            r"^(WIN|FAIL)$": STATEMENT.BOOL_LITERAL,
            r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$": STATEMENT.TYPE_LITERAL,
        }

    def process(self, content):
        content = self._removeIndents(content)
        return self._tokenizeSourceCode(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenizeSourceCode(self, sourceCode):
        for lineIndex, line in enumerate(sourceCode.split("\n")):
            self.currentLineNumber = lineIndex + 1
            self.currentLine = line
            self.currentLineColumnNumber = 0
            self._tokenizeCurrentLine()

    def _tokenizeCurrentLine(self):
        words = self.currentLine.split()

        buffer = ""
        previousLexemeType = None
        isLineTokenized = False

        while not isLineTokenized:
            for word in words:
                if len(buffer) > 0:
                    buffer += " "
                buffer += word

                lexemeType = self._getLexemeType(buffer)
                if lexemeType != None:
                    self.lexemes.append(Token(buffer, lexemeType))
                    previousLexemeType = lexemeType

                    buffer = ""
                    self.currentLineColumnNumber += len(buffer)

            if buffer == "":
                break

            possibleIdentifier, *words = buffer.split()

            if not self._isIdentifier(possibleIdentifier):
                self._throwSyntaxError("Unexpected token")

            identifier = possibleIdentifier

            identifierLexemeType = self._getIdentifierTypeBasedOn(previousLexemeType)

            self.lexemes.append(Token(identifier, identifierLexemeType))
            self.currentLineColumnNumber += len(identifier) + 1
            previousLexemeType = identifierLexemeType

            buffer = ""

    def _throwSyntaxError(self, message):
        syntaxErrorArgs = (
            None,
            self.currentLineNumber,
            self.currentLineColumnNumber,
            self.currentLine,
        )

        raise SyntaxError(message, syntaxErrorArgs)

    def _getLexemeType(self, lexeme):
        allPatterns = dict.keys(self.patternTypes)
        for pattern in allPatterns:
            if re.match(pattern, lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType
        return None

    def _isIdentifier(self, word):
        return re.match(r"^[a-zA-Z]\w*$", word)

    def _getIdentifierTypeBasedOn(self, previousLexemeType):
        variableIdentifierPrecedingLexemeTypes = [
            "variable declaration",
            "variable assignment",
            "addition operation",
            "subtraction operation",
            "multiplication operation",
            "quotient operation",
            "modulo operation",
            "max operation",
            "min operation",
            "and operation",
            "or operation",
            "xor operation",
            "not operation",
            "infinite arity and operation",
            "infinite arity or operation",
            "equal to operation",
            "not equal to operation",
            "concantenation operaion",
            "explicit typecasting keyword",
            "operand seperator",
            "output keyword",
            "input keyword",
            "case keyword",
            "keyword in loop",
            "loop condition keyword",
        ]

        loopIdentifierPrecedingLexemeTypes = [
            "loop declaration and delimeter",
            "loop delimiter",
        ]

        if previousLexemeType == None:
            return "variable identifier"
        if previousLexemeType in variableIdentifierPrecedingLexemeTypes:
            return "variable identifier"
        if previousLexemeType in loopIdentifierPrecedingLexemeTypes:
            return "loop identifier"

        self._throwSyntaxError("Unexpected token")


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType
