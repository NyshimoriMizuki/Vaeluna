class PhonexReader:
    def __init__(self, input) -> None:
        pass


class PhonexLexer:
    def __init__(self, sourcecode: str) -> None:
        self.src = sourcecode
        self.position = 0
        self.last_char = self.next()

    def tokenize(self) -> list['Token']: pass
    def next_token(self) -> 'Token': pass

    def next(self) -> str:
        self.position += 1
        return self.src[self.position]


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
