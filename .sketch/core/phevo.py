from typing import List
import re


from .phonex_reader import PhonexReader, Token


class Phevo(PhonexReader):
    def __init__(self, filename: str):
        super().__init__(filename)

    def evo(self):
        pass
