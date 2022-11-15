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
            r"^IM IN YR$": "loop declaration",
            r"^UPPIN$": "[temp] placeholder",
            r"^NERFIN$": "[temp] placeholder",
            r"^YR$": "[temp] placeholder",
            r"^TIL$": "[temp] placeholder",
            r"^WILE$": "[temp] placeholder",
            r"^IM OUTTA YR$": "[temp] placeholder",
            r"^I HAS A [a-zA-Z]\w*$": "variable identifier",
            r"^IM IN YR [a-zA-Z]\w*$": "loop identifier",
            r"^-?(\d+.\d*|\d*.\d+)$" : "float literal",
            r"^-?\d+$" : "integer literal",
            r"\".*\"" : "string literal",
        }

    def process(self, content):
        content = self._removeIndents(content)
        self._tokenize(content)

    def _removeIndents(self, content):
        return re.sub(r"\t", "", content)

    def _tokenize(self, content):
        for line in content.split("\n"):
            string = ""
            for word in line.split():
                string += word
                lexemeType = self._getLexemeType(string)

                if lexemeType != None:
                    token = Token(string, lexemeType)
                    self.lexemes.append(token)

                    #mema to pre HAHHAHAHAHA ayusin mo na lang
                    if(token.lexemeType == 'variable declaration' and len(line.split()) > 3):
                        string += " "
                    elif(token.lexemeType == 'loop declaration'):
                        string += " "
                    else:
                        string = ""

                else:
                    string += " "

            # if string != "":
            #      print("Syntax error")
            #      break

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
