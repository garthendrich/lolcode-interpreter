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
            r"^-?\d*.\d+$": "float literal",
            r"^-?\d+$": "integer literal",
            r"^\".*\"$": "string literal",
            r"^(WIN|FAIL)$": "bool literal",
            r"^(NOOB|NUMBR|NUMBAR|YARN|TROOF)$": "type literal",
        }

    def process(self, content):
        content = self._removeIndents(content)
        return self._tokenize(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenize(self, content):
        lineNo = 0
        for line in content.split("\n"):
            string = ""
            wordList = line.split()  # list of words
            previousType = None
            lineNo += 1
            while True:
                for word in wordList:
                    string += word
                    lexemeType = self._getLexemeType(string)

                    # print(string + " = " + str(lexemeType))
                    if lexemeType != None:
                        token = Token(string, lexemeType)
                        self.lexemes.append(token)
                        previousType = lexemeType
                        string = ""
                    else:
                        string += " "

                if string != "":
                    wordList = string.split()
                    # checks if previous keyword is part of all patterns or none; none considers the variable being the first lexeme in the line (found in variable assignments)
                    # can be made more specific if allPatterns list are list of keywords where identifiers can be found.
                    if re.match(r"^[a-zA-Z]\w*$", wordList[0]) and (
                        previousType not in ["loop identifier", "variable identifier"]
                        or previousType == None
                    ):
                        if previousType in [
                            "loop declaration and delimeter",
                            "loop delimiter",
                        ]:
                            lexemeType = "loop identifier"
                        else:
                            lexemeType = "variable identifier"

                        token = Token(wordList[0], lexemeType)
                        self.lexemes.append(token)
                        previousType = lexemeType
                        wordList.pop(0)
                        string = ""

                    else:
                        raise SyntaxError(
                            "Unexpected token", (None, lineNo, None, string)
                        )
                else:
                    break
        return "SUCCESS"

    def _getLexemeType(self, lexeme):
        allPatterns = dict.keys(self.patternTypes)
        for pattern in allPatterns:
            if re.match(pattern, lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType
        return None


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType
