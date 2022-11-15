import re


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType


class Interpreter:
    def __init__(self):
        self.lexemes = []
        self.symbolTable = []

        self.patternTypes = {
            r"^HAI$": "code delimiter",
            r"^KTHXBYE$": "code delimiter",
            r"^BTW$": "comment keyword",
            r"^OBTW$": "multiline comment delimiter",
            r"^TLDR$": "multiline comment delimiter",
            r"^I HAS A$": "variable declaration",
            r"^ITZ$": "variable assignment",
            r"^R$": "variable assignment",
            r"^SUM OF$": "arithemtic operation",
            r"^DIFF OF$": "arithemtic operation",
            r"^PRODUKT OF$": "arithemtic operation",
            r"^QUOSHUNT OF$": "arithemtic operation",
            r"^MOD OF$": "arithemtic operation",
            r"^BIGGR OF$": "arithemtic operation",
            r"^SMALLR$": "arithemtic operation",
            r"^BOTH OF$": "boolean operation",
            r"^EITHER OF$": "boolean operation",
            r"^WON OF$": "boolean operation",
            r"^NOT$": "boolean operation",
            r"^ANY OF$": "boolean operation",
            r"^ALL OF$": "boolean operation",
            r"^BOTH SAEM$": "comparison operation",
            r"^DIFFRINT$": "comparison operation",
            r"^SMOOSH$": "concantenation operaion",
            r"^MAEK$": "typecasting keyword",
            r"^A$": "[temp] placeholder",
            r"^IS NOW A$": "[temp] placeholder",
            r"^VISIBLE$": "output keyword",
            r"^GIMMEH$": "input keyword",
            r"^O RLY\?$": "if-then statement keyword",
            r"^YA RLY$": "flow-control statement delimeter",
            r"^MEBBE$": "else-if statement keyword",
            r"^NO WAI$": "[temp] placeholder",
            r"^OIC$": "[temp] placeholder",
            r"^WTF\?$": "[temp] placeholder",
            r"^OMG$": "[temp] placeholder",
            r"^OMGTWF$": "[temp] placeholder",
            r"^IM IN YR$": "[temp] placeholder",
            r"^UPPIN$": "[temp] placeholder",
            r"^NERFIN$": "[temp] placeholder",
            r"^YR$": "[temp] placeholder",
            r"^TIL$": "[temp] placeholder",
            r"^WILE$": "[temp] placeholder",
            r"^IM OUTTA YR$": "[temp] placeholder",
            # r"^I HAS A [a-zA-Z]\w*$": "variable identifier",
            # r"^IM IN YR [a-zA-Z]\w*$": "loop identifier",
        }
        self.allPatterns = dict.keys(self.patternTypes)

    def process(self, content):
        content = self._removeIndents(content)
        self._tokenize(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenize(self, content):
        for line in content.split("\n"):
            string = ""
            lineIndex = 0
            while lineIndex < len(line):
                string += line[lineIndex]
                lexemeType = self._getLexemeType(string)

                lineIndex += 1

                if lexemeType != None:
                    # skip space after lexeme
                    lineIndex += 1

                    token = Token(string, lexemeType)
                    self.lexemes.append(token)

                    string = ""

            # if string != "":
            #     print("Syntax error")
            #     break

    def _getLexemeType(self, lexeme):
        for pattern in self.allPatterns:
            if re.match(f"{pattern}", lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType
        return None


def main():
    interpreter = Interpreter()

    interpreter.process(
        """
HAI
\tI HAS A var
\tI HAS A one ITZ 1
\tvar R SUM OF one AN 2
\tVISIBLE var

\tI HAS A h ITZ "Meow"
\tI HAS A dyM ITZ " "
\tI HAS A ny ITZ "world!!" 
\tVISIBLE SMOOSH h AN dyM AN ny

\tVISIBLE BOTH OF WIN AN FAIL
\tVISIBLE ANY OF WIN AN FAIL AN FAIL MKAY

\tVISIBLE DIFFRINT 4 AN 5

\tMAEK one YARN
\tVISIBLE one

\tFAIL
\tO RLY? 
\t\tYA RLY
\t\t\tVISIBLE ":)"
\t\tNO WAI
\t\t\tVISIBLE ":("
\tOIC

\tIT R "b"
\tWTF?
\tOMG "a"
\t\tVISIBLE "it's a"
\tOMG "b"
\t\tVISIBLE "it's b"
\tOMG "c"
\t\tVISIBLE "it's c"
\tOMGWTF
\t\tVISIBLE "it's something else"
\tOIC

\tI HAS A index ITZ 0
\tIM IN YR hous UPPIN YR index TIL BOTH SAEM index AN 5
\t\tVISIBLE SMOOSH "iteration " AN index
\tIM OUTTA YR hous
KTHXBYE
"""
    )

    # test
    for token in interpreter.lexemes:
        print(f"{str.ljust(token.lexeme, 16)} {token.lexemeType}")


if __name__ == "__main__":
    main()
