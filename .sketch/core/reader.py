from typing import Optional, List
from abc import ABC, abstractmethod


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


class Reader(ABC):
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf8") as f:
            self.file_content = f.read()

    @abstractmethod
    def tokenize(self):
        return self.file_content.split()
