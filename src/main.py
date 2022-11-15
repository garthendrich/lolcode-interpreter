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
            "HAI": "code delimiter",
            "KTHXBYE": "code delimiter",
            "BTW": "comment keyword",
            "OBTW": "multiline comment delimiter",
            "TLDR": "multiline comment delimiter",
            "I HAS A": "variable declaration",
            "ITZ": "variable assignment",
            "\bR\b": "variable assignment",
            "SUM OF": "arithemtic operation",
            "DIFF OF": "arithemtic operation",
            "PRODUKT OF": "arithemtic operation",
            "QUOSHUNT OF": "arithemtic operation",
            "MOD OF": "arithemtic operation",
            "BIGGR OF": "arithemtic operation",
            "SMALLR": "arithemtic operation",
            "BOTH OF": "boolean operation",
            "EITHER OF": "boolean operation",
            "WON OF": "boolean operation",
            # "NOT": "boolean operation",
            # "ANY OF": "boolean operation",
            # "ALL OF": "boolean operation",
            # "BOTH SAEM": "comparison operation",
            # "DIFFRINT": "comparison operation",
            # "SMOOSH": "concantenation operaion",
            # "MAEK": "typecasting keyword",
            # "\bA\b": "[temp] placeholder",
            # "IS NOW A": "[temp] placeholder",
            # "VISIBLE": "output keyword",
            # "GIMMEH": "input keyword",
            # "O RLY\?": "if-then statement keyword",
            # "YA RLY": "flow-control statement delimeter",
            # "MEBBE": "else-if statement keyword",
            # "NO WAI": "[temp] placeholder",
            # "OIC": "[temp] placeholder",
            # "WTF\?": "[temp] placeholder",
            # "OMG": "[temp] placeholder",
            # "OMGTWF": "[temp] placeholder",
            # "IM IN YR": "[temp] placeholder",
            # "UPPIN": "[temp] placeholder", 
            # "NERFIN": "[temp] placeholder", 
            # "YR": "[temp] placeholder",
            # "TIL": "[temp] placeholder",
            # "WILE": "[temp] placeholder",
            # "IM OUTTA YR": "[temp] placeholder",
            # "I HAS A ([a-zA-Z]\w*)": "variable identifier",
            # "IM IN YR ([a-zA-Z]\w*)": "loop identifier",
        }
        self.allPatterns = dict.keys(self.patternTypes)

    def process(self, content):
        self.tokenize(content)

    def tokenize(self, content):
        lexemes = re.findall("|".join(self.allPatterns), content)
        print(lexemes)
        for lexeme in lexemes:
            lexemeType = self.getLexemeType(lexeme)
            token = Token(lexeme, lexemeType)
            self.lexemes.append(token)

    def getLexemeType(self, lexeme):
        for pattern in self.allPatterns:
            if re.match(f"^{pattern}$", lexeme):
                lexemeType = self.patternTypes[pattern]
                return lexemeType


def main():
    interpreter = Interpreter()

    # sample code reference
    # https://www.tutorialspoint.com/lolcode/lolcode_some_more_examples.htm
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
    for token in interpreter.lexemes:
        print(f"{str.ljust(token.lexeme, 16)} {token.lexemeType}")


if __name__ == "__main__":
    main()
