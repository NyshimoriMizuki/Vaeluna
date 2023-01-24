from typing import Optional

from ..setupcl import SetupCL


EOF = "\0"
WHITESPACE = {
    " ": "SPACE",
    "\n": "NEW_LINE",
    "\t": "TAB"
}
BRACKETS = {
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

        if char == EOF:
            return self.__assign_and_return(Token("EOF"))

        if self.last_token == Token("IDENT") and not char in '->{}→ \n\t':
            self.tokenized[-1].add_value(char)
            return

        if char in ['>', '-', '→']:
            if char == '-' and self.is_in_nexts(">", range=1):
                self.advance(1)
            return self.__assign_and_return(Token("OPER", "TO"))
        elif char in " \t\n":
            return self.__assign_and_return(Token(WHITESPACE[char]))
        elif char in "{}":
            return self.__assign_and_return(Token(BRACKETS[char]))
        elif char.isupper():
            return self.__assign_and_return(Token("IDENT", char))
        elif char in self.phonemes:
            return self.__assign_and_return(Token("PHONE", char))
        elif char in self.phonemes:
            return self.__assign_and_return(Token("PHONE", char))
        else:
            return f'!{char}'

    def __assign_and_return(self, token: 'Token'):
        self.last_token = token
        return token

    def next(self) -> str:
        self.position += 1
        if not self.position < len(self.src):
            return EOF
        return self.src[self.position]

    def is_in_nexts(self, target, range: int = 10):
        """
        check if is `target` in the nexts in a `range`

        is add `1` in `range`
        """
        return target in self.src[self.position:self.position+range+1]

    def advance(self, num: int = 1): self.position += 1


class PhonexParser:
    def __init__(self) -> None:
        pass


class Token:
    def __init__(self, type: str, value: str = None) -> None:
        self.type = type.upper()
        self.value = value

    def __repr__(self) -> str:
        if self.value:
            return f"<{self.type};{self.value}>"
        return f"<{self.type}>"

    def __eq__(self, __o: 'Token') -> bool:
        if self.type == __o.type:
            return True
        return False

    def add_value(self, value):
        if self.value:
            self.value += value
        else:
            self.value = value

    def if_blank(self, condition: bool, token: 'Token'):
        if self.type == "BLANK" and condition:
            self.type, self.value = token.type, token.value
        return self

    def elif_blank(self, condition: bool, token: 'Token'):
        return self.if_blank(condition, token)

    def else_blank(self, token: 'Token'):
        return self.if_blank(True, token)


def join_lists(lists):
    return [element for list_ in lists for element in list_]
