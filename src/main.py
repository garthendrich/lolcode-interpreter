import re


class Token:
    def __init__(self, lexeme, lexemeType):
        self.lexeme = lexeme
        self.lexemeType = lexemeType


class Interpreter:
    def __init__(self):
        self.symbolTable = []

        self.patternTypes = {
            "HAI": "keyword",
            "KTHXBYE": "keyword",
            "BTW": "keyword",
            "OBTW": "keyword",
            "TLDR": "keyword",
            "I HAS A": "keyword",
            # more here
            "[a-zA-Z]\w*": "identifier",
        }
        self.allPatterns = dict.keys(self.patternTypes)

    def process(self, content):
        self.tokenize(content)

    def tokenize(self, content):
        lexemes = re.findall("|".join(self.allPatterns), content)
        for lexeme in lexemes:
            lexemeType = self.getLexemeType(lexeme)
            token = Token(lexeme, lexemeType)
            self.symbolTable.append(token)

    def getLexemeType(self, lexeme):
        for pattern in self.allPatterns:
            if re.match(f"^{pattern}$", lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType


def main():

    interpreter = Interpreter()
    interpreter.process(
        """
HAI 1.2
HOW IZ I POWERTWO YR NUM
    BTW RETURN 1 IF 2 TO POWER OF 0
    BOTH SAEM NUM AN 0, O RLY?
        YA RLY, FOUND YR 1
    OIC

    BTW CALCULATE 2 TO POWER OF NUM
    I HAS A INDEX ITZ 0
    I HAS A TOTAL ITZ 1
    IM IN YR LOOP UPPIN YR INDEX TIL BOTH SAEM INDEX AN NUM
        TOTAL R PRODUKT OF TOTAL AN 2
    IM OUTTA YR LOOP

    FOUND YR TOTAL
    IF U SAY SO
    BTW OUTPUT: 8
    VISIBLE I IZ POWERTWO YR 4 MKAY
KTHXBYE
"""
    )

    # test
    for token in interpreter.symbolTable:
        print(f"{str.ljust(token.lexeme, 16)} {token.lexemeType}")


if __name__ == "__main__":
    main()
