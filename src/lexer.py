import re

class Lexer:
    def __init__(self):
        self.lexemes = []

        self.patternTypes = {
            r"^HAI$": "code delimiter",
            r"^KTHXBYE$": "code delimiter",
            r"^BTW$": "comment keyword",
            r"^OBTW$": "multiline comment delimiter",
            r"^TLDR$": "multiline comment delimiter",
            r"^I HAS A$": "variable declaration",
            r"^ITZ$": "variable assignment",
            r"^R$": "variable assignment",
            r"^SUM OF$": "addition operation",
            r"^DIFF OF$": "subtraction operation",
            r"^PRODUKT OF$": "multiplication operation",
            r"^QUOSHUNT OF$": "quotient operation",
            r"^MOD OF$": "modulo operation",
            r"^BIGGR OF$": "max operation",
            r"^SMALLR$": "min operation",
            r"^BOTH OF$": "and operation",
            r"^EITHER OF$": "or operation",
            r"^WON OF$": "xor operation",
            r"^NOT$": "not operation",
            r"^ANY OF$": "infinite arity and operation",
            r"^ALL OF$": "infinite arity or operation",
            r"^BOTH SAEM$": "equal to operation",
            r"^DIFFRINT$": "not equal to operation",
            r"^SMOOSH$": "concantenation operaion",
            r"^MAEK$": "explicit typecasting keyword",
            r"^A$": "optional A keyword",
            r"^AN$": "operand seperator",
            r"^IS NOW A$": "re-casting keyword",
            r"^VISIBLE$": "output keyword",
            r"^GIMMEH$": "input keyword",
            r"^O RLY\?$": "if-else delimeter",
            r"^YA RLY$": "if statement",
            r"^MEBBE$": "else-if statement keyword",
            r"^NO WAI$": "else statement keyword",
            r"^OIC$": "flow-control statements delimeter",
            r"^WTF\?$": "switch-case statement delimeter",
            r"^OMG$": "case keyword",
            r"^OMGTWF$": "default case keyword",
            r"^IM IN YR$": "loop declaration and delimeter",
            r"^UPPIN$": "increment keyword",
            r"^NERFIN$": "decrement keyword",
            r"^YR$": "keyword in loop",
            r"^TIL$": "loop condition keyword",
            r"^WILE$": "loop condition keyword",
            r"^IM OUTTA YR$": "loop delimiter",
            r"^-?\d*.\d+$" : "float literal",
            r"^-?\d+$" : "integer literal",
            r"^\".*\"$" : "string literal",
            r"^(WIN|FAIL)$" : "bool literal",
            r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$" : "type literal",
        }

    def process(self, content):
        content = self._removeIndents(content)
        return self._tokenizeSourceCode(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenizeSourceCode(self, sourceCode):
        for lineIndex, line in enumerate(sourceCode.split("\n")):
            self.currentLineNumber = lineIndex + 1
            self._tokenizeLine(line)

    def _tokenizeLine(self, line):
        words = line.split()

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

            if buffer == "":
                break

            possibleIdentifier, *words = buffer.split()

            if not self._isIdentifier(possibleIdentifier):
                raise SyntaxError(
                    "Unexpected token",
                    (None, self.currentLineNumber, None, possibleIdentifier),
                )

            identifier = possibleIdentifier

            identifierLexemeType = self._getIdentifierTypeBasedOn(previousLexemeType)

            self.lexemes.append(Token(identifier, identifierLexemeType))
            previousLexemeType = identifierLexemeType

            buffer = ""

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
        if previousLexemeType in ["loop identifier", "variable identifier"]:
            raise SyntaxError(
                "Unexpected token", (None, self.currentLineNumber, None, "")
            )

        if previousLexemeType in ["loop declaration and delimeter", "loop delimiter"]:
            return "loop identifier"

        return "variable identifier"


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType