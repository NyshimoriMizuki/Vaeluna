from typing import Optional, Union

from ..setupcl import SetupCL
from .nodes import *


EOF = "\0"
WHITESPACE_AND_BRACKETS = {
    " ": "SPACE",
    "\n": "NEW_LINE",
    "\t": "TAB",
    "{": "OPEN_SET",
    "}": "CLOSE_SET"
}
DIACRITICS = "̹̜̟̠̺̻̝˔̞˕ː̄˞̩̬ᶲᵝʰʲʷ̯̥̆̃ⁿ̤ʱˤˠᵐᶬᶯᶮᵑᶰʼ̊"


class PhonexReader:
    def __init__(self, input) -> None:
        pass


class PhonexLexer:
    def __init__(self, sourcecode: str) -> None:
        self.src = sourcecode
        self.position = -1
        self.last_token = Token("EOF")
        self.tokenized: list['Token'] = []
        self.in_expr = False
        self.open_comment = False

    @ staticmethod
    def from_file(filename) -> 'PhonexLexer':
        with open(filename, 'r', encoding='utf8') as f:
            return PhonexLexer(f.read())

    def tokenize(self) -> list['Token']:
        while self.position < len(self.src):
            if new_token := self.next_token():
                self.last_token = new_token
                self.tokenized.append(new_token)
        return self.tokenized

    def next_token(self) -> Optional['Token']:
        char = self.next()

        if (self.open_comment and char != '"') or \
                (char in DIACRITICS and self.last_token == Token("PHONE")):
            self.tokenized[-1].add_value(char)
            return

        if char == "\n":
            self.in_expr = False
        elif char == "/":
            self.in_expr = True
        elif char == '"':
            self.open_comment = not self.open_comment
        elif self.nexts_equal_to("->"):
            char = '→'
        elif self.nexts_equal_to(" - "):
            char = '—'

        return (
            Token("blank")
            .if_blank(char == EOF, Token("EOF"))
            .elif_blank(char == '"',
                        Token("COMMENT" if self.open_comment else "END_COMMENT"))
            .elif_blank(char == "/", Token("EXPR"))
            .elif_blank(char == "—", Token("IN_LABEL"))
            .elif_blank(char in ">→", Token("OPER", "TO"))
            .elif_blank((self.nexts_equal_to("or")) and self.in_expr,
                        Token("OPER", "OR"))
            .elif_blank(char in "!#_%@:", Token("OPER", char))
            .elif_blank(char in " \t\n{}", Token(WHITESPACE_AND_BRACKETS.get(char)))
            .elif_blank(self.nexts_equal_to("filter"), Token("KEY", "filter"))
            .elif_blank(self.nexts_equal_to("group"), Token("KEY", "group"))
            .elif_blank(self.nexts_equal_to("all"), Token("KEY", "all"))
            .elif_blank(self.nexts_equal_to("consonants"), Token("KEY", "consonants"))
            .elif_blank(self.nexts_equal_to("vowels"), Token("KEY", "vowels"))
            .elif_blank(char.isupper(), Token("IDENT", char))
            .else_blank(Token("PHONE", char))
        )

    def next(self) -> str:
        self.position += 1
        if not self.position < len(self.src):
            return EOF
        return self.src[self.position]

    def nexts_equal_to(self, target: str) -> bool:
        """
        check if `target` is in the nexts chars
        """
        if target in self.src[self.position-1:self.position+len(target)]:
            self.position += len(target)-1
            return True
        return False


class PhonexParser:
    def __init__(self, setup: SetupCL, tokens: list['Token']) -> None:
        self.phonemes = join_lists(setup.phonemes.values())
        self.tokens = tokens
        self.ast = []

    def parse(self):
        pass

    def agglutinate(self):
        list_res = []
        last_token = Token("blank")
        for current_token in self.tokens:
            current_token = Token("WHITESPACE") if current_token.is_("TAB") or \
                current_token.is_("SPACE") else current_token

            if self.compare(last_token, current_token,  # and they in
                            [Token("PHONE"), Token("WHITESPACE"), Token("NEW_LINE")]):
                last_token.join(current_token)
                continue
            last_token = current_token
            list_res.append(last_token)
        self.tokens = list_res

    @staticmethod
    def compare(_1: 'Token', _2: 'Token', agglutinate_tokens_list: list['Token']):
        return _1 in agglutinate_tokens_list and _2 == _1


class Token:
    def __init__(self, type: str, value: str = None) -> None:
        self.type = str(type).upper()
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"<{self.type};{self.value}>"
        return f"<{self.type}>"

    def __eq__(self, __o: 'Token') -> bool:
        return self.type == __o.type

    def add_value(self, value):
        self.value = (self.value if self.value else "") + value

    def join(self, token: 'Token'):
        if self.value and token.value:
            self.value += token.value

    def if_blank(self, condition: bool, token: 'Token'):
        if self.type == "blank".upper() and condition:
            self.type, self.value = token.type, token.value
        return self

    def elif_blank(self, condition: bool, token: 'Token'):
        return self.if_blank(condition, token)

    def else_blank(self, token: 'Token'):
        return self.if_blank(True, token)

    def is_(self, token: Union['Token', str]):
        if type(token) == str:
            return self.type == token
        return token == self


def join_lists(lists):
    return [element for list_ in lists for element in list_]
