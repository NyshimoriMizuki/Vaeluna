from typing import Optional, List, Union
import re


class Token:
    def __init__(self, type_, value: Optional[str] = None):
        self.type = type_
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"<{self.type}; {self.value}>"
        return f"<{self.type}>"

    def __eq__(self, __o: object) -> bool:
        if __o.type == self.type:
            return True
        return False

    def join(self, extra_char):
        if not self.value:
            self.value = ""
        self.value += extra_char

    def change_type(self, new_type):
        self.type = new_type

    def if_blank(self, expr: bool, value: 'Token'):
        if self.type == "blank":
            if type(value) == Token and expr:
                self.type, self.value = value.type, value.value
        return self

    def elif_blank(self, expr: bool, value: 'Token'):
        return self.if_blank(expr, value)

    def else_blank(self, value: 'Token'):
        return self.if_blank(True, value)

    def equal_to(self, value):
        return self == Token(value)


class Reader:
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf8") as f:
            self.file_content = f.read()

    def tokenize(self):
        open_phonex = False
        tokenized: List[Token] = [Token("START")]

        for char in self.file_content:
            if char == '/':
                open_phonex = not open_phonex
                continue

            if (tokenized[-1].equal_to("PHONEX") and open_phonex) or \
                    (tokenized[-1].equal_to("IDENT") and re.match("[a-zA-Z_]", char)):
                tokenized[-1].join(char)
            else:
                tokenized.append(
                    Token("blank")
                    .if_blank(open_phonex, Token("PHONEX", char))
                    .elif_blank(char in "=:", Token("OPERATOR", char))
                    .elif_blank(char == " ", Token("SPACE"))
                    .elif_blank(char == "\n", Token("NEW_LINE"))
                    .elif_blank(char == "\t", Token("TAB"))
                    .elif_blank(char == "{", Token("L_PARAM"))
                    .elif_blank(char == "}", Token("R_PARAM"))
                    .else_blank(Token("IDENT", char))
                )

        def is_keyword(x: Token):
            if x.value in ["group", "filter", "if", "do", "or", "is", "all"]:
                return Token("KEYWORD", x.value)
            return x
        return map(is_keyword, tokenized)

        #

        #
        # "jaɽ·ˈsiɽ", "wi·wa·ˈbe", "ŋoɽ·iw·ˈaj", "ˈkaw·o·na", "ˈa"
        # "jaɽ·ˈsiɽ", "wi·wa·ˈbe", "ŋoɽ·ʔi·ˈwaj", "ˈkaw·ʔo·na", "ˈa"
