from typing import List
import re

from .reader import Token, Reader


class FormatterReader(Reader):
    def __init__(self, filename: str):
        super().__init__(filename)

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
