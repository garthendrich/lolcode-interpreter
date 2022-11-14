import re


class Interpreter:
    def __init__(self):
        keywords = ["HAI", "KTHXBYE", "BTW", "OBTW", "TLDR", "I HAS A"]
        identifierPattern = "[a-zA-Z]\w*"
        self.patterns = [*keywords, identifierPattern]

    def process(self, content):
        self.tokenize(content)

    def tokenize(self, content):
        self.tokens = re.findall("|".join(self.patterns), content)


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

    print(interpreter.tokens)


if __name__ == "__main__":
    main()
