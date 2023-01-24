from ..setupcl import SetupCL


class PhonexReader:
    def __init__(self, input) -> None:
        pass


class PhonexLexer:
    def __init__(self, sourcecode: str, setup: SetupCL) -> None:
        self.src = sourcecode
        self.position = 0
        self.last_char = self.next()
        self.phonemes = join_lists(setup.phonemes.values())

    @ staticmethod
    def from_file(filename) -> 'PhonexLexer':
        with open(filename, 'r', encoding='utf8') as f:
            return PhonexLexer(f.read())

    def tokenize(self) -> list['Token']:
        tokens = []
        while self.position < len(self.src):
            tokens.append(self.next_token())

    def next_token(self) -> 'Token': pass

    def next(self) -> str:
        self.position += 1
        return self.src[self.position]

    def advance(self, num: int = 1): self.position += 1


class PhonexParser:
    def __init__(self) -> None:
        pass


class Token:
    def __init__(self, type: str, value: str) -> None:
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


def join_lists(lists):
    return [element for list_ in lists for element in list_]
