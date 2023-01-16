from typing import List
import re


from .reader import Reader, Token


class PhevoReader(Reader):
    def __init__(self, filename: str):
        super().__init__(filename)

    def tokenize(self):
        open_comment = False
        tokenized: List[Token] = [Token("START")]

        for char in self.file_content:
            if char in '"':
                open_comment = not open_comment
                continue

            if tokenized[-1].equal_to("OPERATOR") and char in "!#%>" or \
                    (tokenized[-1].equal_to("COMMENT") and open_comment) or \
                    (tokenized[-1].equal_to("IDENT") and not char in "!%#:{} \t\n"):
                tokenized[-1].join(char)
            else:
                tokenized.append(
                    Token("blank")
                    .if_blank(open_comment, Token("COMMENT", char))
                    .elif_blank(char in "#:/=—->→@%!,_", Token("OPERATOR", char))
                    .elif_blank(char in "0*∅", Token("PHONEME_NULL"))
                    .elif_blank(char == " ", Token("SPACE"))
                    .elif_blank(char == "\n", Token("NEW_LINE"))
                    .elif_blank(char == "\t", Token("TAB"))
                    .elif_blank(char == "(", Token("L_PARAM"))
                    .elif_blank(char == ")", Token("R_PARAM"))
                    .elif_blank(char == "{", Token("L_BRACKET"))
                    .elif_blank(char == "}", Token("R_BRACKET"))
                    .elif_blank(char == "[", Token("L_SQ_BRACKET"))
                    .elif_blank(char == "]", Token("R_SQ_BRACKET"))
                    .else_blank(Token("IDENT", char))
                )

        def rename_keywords(x: Token):
            if x.value in ["group", "or", "all"]:
                return Token("KEYWORD", x.value)
            return x

        def no_space_token(x: Token):
            return False if x == Token("SPACE") else True
        return map(rename_keywords, filter(no_space_token, tokenized))
