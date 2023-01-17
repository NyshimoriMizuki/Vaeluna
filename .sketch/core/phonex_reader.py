from typing import Optional, List
from abc import ABC, abstractmethod

from .setupcl import SetupCL


WHITESPACE = {
    " ": "SPACE",
    "\n": "NEW_LINE",
    "\t": "TAB"
}
BLOCKS = {
    "(": "L_PARAM",
    ")": "R_PARAM",
    "{": "L_BRACKET",
    "}": "R_BRACKET",
    "[": "L_SQ_BRACKET",
    "]": "R_SQ_BRACKET"
}


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


class PhonexReader:
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf8") as f:
            self.file_content = f.read()

    def tokenize(self):
        open_comment = False
        tokens: List[Token] = [Token("START")]

        for char in self.file_content:
            if char in '"':
                open_comment = not open_comment
                continue

            if tokens[-1].equal_to("OPERATOR") and char in ">" or \
                    (tokens[-1].equal_to("COMMENT") and open_comment) or \
                    (tokens[-1].equal_to("IDENT") and not char in "!%#:{} \t\n"):
                tokens[-1].join(char)
            else:
                tokens.append(
                    Token("blank")
                    .if_blank(open_comment, Token("COMMENT", char))
                    .elif_blank(char == "/", Token("SEPARATOR"))
                    .elif_blank(char in "#:=—->→@%!,_", Token("OPERATOR", char))
                    .elif_blank(char in "0*∅", Token("PHONEME_NULL"))
                    .elif_blank(char in " \n\t", Token(WHITESPACE.get(char)))
                    .elif_blank(char in "({[]})", Token(BLOCKS.get(char)))
                    .else_blank(Token("IDENT", char))
                )

        return filter(filter_spaces, map(rename_keywords, tokens))

    def generate_ast(self, setup: SetupCL):
        pass


class BaseNode(ABC):
    def __init__(self, content=None):
        self.content = content

    @abstractmethod
    def __repr__(self) -> str:
        return f"content: {{ {self.content} }}"


class StartNode(BaseNode):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return "Start {}"


class GroupNode(BaseNode):
    def __init__(self, name: str, value: list[str]):
        self.id = name
        self.value = value

    def __repr__(self) -> str:
        return f"Group {{ id: {self.id} value: {self.value} }}"


class PhonexNode(BaseNode):
    def __init__(self, left: list, right: list, condition: list):
        self.left = left
        self.right = right
        self.condition = condition

    def __repr__(self) -> str:
        return f"PhonemeExpression {{ condition: {self.condition}, left: {self.left}, right: {self.right} }}"


class StopCommentNode(BaseNode):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return f"StopComment {{ message: {self.message} }}"


class LabelNode(BaseNode):
    def __init__(self, type, name, content):
        self.type = type
        self.name = name
        self.content = content

    def __repr__(self) -> str:
        return f"Label {{type: {self.type}, name: {self.name}, content: {self.content} }}"


def filter_spaces(x):
    if x.type == "SPACE":
        return False
    return True


def rename_keywords(x: Token):
    if x.value in ["group", "or", "all"]:
        return Token("KEYWORD", x.value)
    return x
