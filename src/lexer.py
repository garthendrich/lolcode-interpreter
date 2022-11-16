import re


# enum
class STATEMENT_TYPE:
    expression = "expression"
    variable_identifier = "variable_identifier"
    loop_identifier = "loop_identifier"
    function_identifier = "function_identifier"


class Lexer:
    def __init__(self):
        self.lexemes = []

        self.patternsData = {
            r"^HAI$": {
                "lexemeType": "code delimiter",
                "next": None,
            },
            r"^KTHXBYE$": {
                "lexemeType": "code delimiter",
                "next": None,
            },
            r"^BTW$": {
                "lexemeType": "comment keyword",
                "next": None,
            },
            r"^OBTW$": {
                "lexemeType": "multiline comment delimiter",
                "next": None,
            },
            r"^TLDR$": {
                "lexemeType": "multiline comment delimiter",
                "next": None,
            },
            r"^I HAS A$": {
                "lexemeType": "variable declaration",
                "next": STATEMENT_TYPE.variable_identifier,
            },
            r"^ITZ$": {
                "lexemeType": "variable assignment",
                "next": STATEMENT_TYPE.expression,
            },
            r"^R$": {
                "lexemeType": "variable assignment",
                "next": STATEMENT_TYPE.expression,
            },
            r"^SUM OF$": {
                "lexemeType": "addition operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^DIFF OF$": {
                "lexemeType": "subtraction operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^PRODUKT OF$": {
                "lexemeType": "multiplication operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^QUOSHUNT OF$": {
                "lexemeType": "quotient operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^MOD OF$": {
                "lexemeType": "modulo operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^BIGGR OF$": {
                "lexemeType": "max operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^SMALLR OF$": {
                "lexemeType": "min operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^BOTH OF$": {
                "lexemeType": "and operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^EITHER OF$": {
                "lexemeType": "or operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^WON OF$": {
                "lexemeType": "xor operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^NOT$": {
                "lexemeType": "not operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^ANY OF$": {
                "lexemeType": "infinite arity and operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^ALL OF$": {
                "lexemeType": "infinite arity or operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^BOTH SAEM$": {
                "lexemeType": "equal to operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^DIFFRINT$": {
                "lexemeType": "not equal to operation",
                "next": STATEMENT_TYPE.expression,
            },
            r"^SMOOSH$": {
                "lexemeType": "concantenation operaion",
                "next": STATEMENT_TYPE.expression,
            },
            r"^MAEK$": {
                "lexemeType": "explicit typecasting keyword",
                "next": STATEMENT_TYPE.expression,
            },
            r"^A$": {
                "lexemeType": "optional A keyword",
                "next": None,
            },
            r"^AN$": {
                "lexemeType": "operand seperator",
                "next": STATEMENT_TYPE.expression,
            },
            r"^IS NOW A$": {
                "lexemeType": "re-casting keyword",
                "next": None,
            },
            r"^VISIBLE$": {
                "lexemeType": "output keyword",
                "next": STATEMENT_TYPE.expression,
            },
            r"^GIMMEH$": {
                "lexemeType": "input keyword",
                "next": STATEMENT_TYPE.variable_identifier,
            },
            r"^O RLY\?$": {
                "lexemeType": "if-else delimeter",
                "next": None,
            },
            r"^YA RLY$": {
                "lexemeType": "if statement",
                "next": None,
            },
            r"^MEBBE$": {
                "lexemeType": "else-if statement keyword",
                "next": None,
            },
            r"^NO WAI$": {
                "lexemeType": "else statement keyword",
                "next": None,
            },
            r"^OIC$": {
                "lexemeType": "flow-control statements delimeter",
                "next": None,
            },
            r"^WTF\?$": {
                "lexemeType": "switch-case statement delimeter",
                "next": None,
            },
            r"^OMG$": {
                "lexemeType": "case keyword",
                "next": STATEMENT_TYPE.expression,
            },
            r"^OMGTWF$": {
                "lexemeType": "default case keyword",
                "next": None,
            },
            r"^IM IN YR$": {
                "lexemeType": "loop declaration and delimeter",
                "next": STATEMENT_TYPE.loop_identifier,
            },
            r"^UPPIN$": {
                "lexemeType": "increment keyword",
                "next": None,
            },
            r"^NERFIN$": {
                "lexemeType": "decrement keyword",
                "next": None,
            },
            r"^YR$": {
                "lexemeType": "keyword in loop",
                "next": STATEMENT_TYPE.variable_identifier,
            },
            r"^TIL$": {
                "lexemeType": "loop condition keyword",
                "next": STATEMENT_TYPE.expression,
            },
            r"^WILE$": {
                "lexemeType": "loop condition keyword",
                "next": STATEMENT_TYPE.expression,
            },
            r"^IM OUTTA YR$": {
                "lexemeType": "loop delimiter",
                "next": None,
            },
        }

        self.literalPatternsData = {
            r"^-?\d*.\d+$": {
                "lexemeType": "float literal",
                "next": None,
            },
            r"^-?\d+$": {
                "lexemeType": "integer literal",
                "next": None,
            },
            r"^\".*\"$": {
                "lexemeType": "string literal",
                "next": None,
            },
            r"^(WIN|FAIL)$": {
                "lexemeType": "bool literal",
                "next": None,
            },
        }

    def process(self, content):
        content = self._removeIndents(content)
        return self._tokenize(content)
        #self._tokenize(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenize(self, content):
        for line in content.split("\n"):
            string = ""
            next = None
            for word in line.split():
                string += word

                if next == STATEMENT_TYPE.function_identifier:
                    token = self._getMatchedIdentifierToken(
                        string, "function identifier"
                    )
                    if token is not None:
                        self.lexemes.append(token)
                        string = ""
                        next = None
                    else:
                        print(f"Syntax error {string}")

                    continue

                if next == STATEMENT_TYPE.loop_identifier:
                    token = self._getMatchedIdentifierToken(string, "loop identifier")
                    if token is not None:
                        self.lexemes.append(token)
                        string = ""
                        next = None
                    else:
                        print(f"Syntax error {string}")

                    continue

                if next == STATEMENT_TYPE.variable_identifier:
                    token = self._getMatchedIdentifierToken(
                        string, "variable identifier"
                    )
                    if token is not None:
                        self.lexemes.append(token)
                        string = ""
                        next = None
                    else:
                        print(f"Syntax error {string}")

                    continue

                if next == STATEMENT_TYPE.expression:
                    token = self._getMatchedIdentifierToken(
                        string, "variable identifier"
                    )
                    if token is not None:
                        self.lexemes.append(token)
                        string = ""
                        next = None
                        continue

                    lexemeData = self._getMatchedLiteralData(string)
                    if lexemeData is None:
                        # print(f"Syntax error {string}")
                        pass
                    else:
                        lexemeType = lexemeData["lexemeType"]
                        token = Token(string, lexemeType)
                        self.lexemes.append(token)
                        string = ""
                        continue

                lexemeData = self._findMatchedLexemeData(string)

                if lexemeData == None:
                    string += " "
                    continue

                lexemeType = lexemeData["lexemeType"]
                token = Token(string, lexemeType)
                self.lexemes.append(token)

                next = lexemeData["next"]

                string = ""

            if string != "":
                #return ("Syntax error " + string)
                pass
        
        return "SUCCESS"        

    def _findMatchedLexemeData(self, string):
        allPatterns = dict.keys(self.patternsData)
        for pattern in allPatterns:
            if re.match(pattern, string):
                lexemeType = self.patternsData[pattern]
                return lexemeType
        return None

    def _getMatchedIdentifierToken(self, string, lexemeType):
        if re.match("^[a-zA-Z]\w*$", string):
            return Token(string, lexemeType)

        return None

    def _getMatchedLiteralData(self, string):
        allLiteralPatterns = dict.keys(self.literalPatternsData)
        for pattern in allLiteralPatterns:
            if re.match(pattern, string):
                lexemeType = self.literalPatternsData[pattern]
                return lexemeType
        return None


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType
