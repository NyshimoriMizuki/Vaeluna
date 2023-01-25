from typing import Optional

from ..setupcl import SetupCL


EOF = "\0"
WHITESPACE_AND_BRACKETS = {
    " ": "SPACE",
    "\n": "NEW_LINE",
    "\t": "TAB",
    "{": "OPEN_SET",
    "}": "CLOSE_SET"
}


class PhonexReader:
    def __init__(self, input) -> None:
        pass


class PhonexLexer:
    def __init__(self, sourcecode: str, setup: SetupCL) -> None:
        self.src = sourcecode
        self.position = -1
        self.last_token = Token("EOF")
        self.phonemes = join_lists(setup.phonemes.values())
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
                self.tokenized.append(new_token)
        return self.tokenized

    def next_token(self) -> Optional['Token']:
        char = self.next()

        if (self.last_token == Token("IDENT") and not char in '>{}→ \n\t') or \
                (self.open_comment and char != '"'):
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

        return self.__assign_and_return(
            Token("blank")
            .if_blank(char == EOF, Token("EOF"))
            .elif_blank(char == '"',
                        Token("COMMENT" if self.open_comment else "END_COMMENT"))
            .elif_blank(char == "/", Token("EXPR"))
            .elif_blank(char in ">→", Token("OPER", "TO"))
            .elif_blank((self.nexts_equal_to("or")) and self.in_expr,
                        Token("OPER", "OR"))
            .elif_blank(char in "!#_%@", Token("OPER", char))
            .elif_blank(char in " \t\n{}", Token(WHITESPACE_AND_BRACKETS.get(char)))
            .elif_blank(self.nexts_equal_to("filter"), Token("KEY", "filter"))
            .elif_blank(self.nexts_equal_to("group"), Token("KEY", "group"))
            .elif_blank(char.isupper(), Token("IDENT", char))
            .elif_blank(self.__char_is_in_phonemes_or_coarticulation(char),
                        Token("PHONE", self.__find_phoneme()))
            .else_blank(Token("PHONE", char))
        )

    def __find_phoneme(self) -> Optional[str]:
        for phoneme in sorted(self.phonemes, key=len, reverse=True):
            if self.nexts_equal_to(phoneme):
                return phoneme

    def __assign_and_return(self, token: 'Token') -> 'Token':
        self.last_token = token
        return token

    def __char_is_in_phonemes_or_coarticulation(self, char: str) -> bool:
        for i in self.phonemes:
            if char in i:
                return True
        return False

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
    def __init__(self) -> None:
        pass


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

    def if_blank(self, condition: bool, token: 'Token'):
        if self.type == "blank".upper() and condition:
            self.type, self.value = token.type, token.value
        return self

    def elif_blank(self, condition: bool, token: 'Token'):
        return self.if_blank(condition, token)

    def else_blank(self, token: 'Token'):
        return self.if_blank(True, token)


def join_lists(lists):
    return [element for list_ in lists for element in list_]
