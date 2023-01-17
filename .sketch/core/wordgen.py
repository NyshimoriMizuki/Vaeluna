from random import choice, randrange
from typing import List

from .setupcl import SetupCL
from .phonex_reader import PhonexReader


class WordGenerator:
    def __init__(self, setup: SetupCL):
        self.phonemes = setup.phonemes
        self.max_word_length = setup.word_length
        self.syllable_struct = self.__break_into_list(setup.syllable_struct)

    def generate(self, num: int = 1):
        words = []
        for _ in range(num):
            random_length = randrange(0, self.max_word_length) + 1
            stress_place = randrange(0, random_length)

            new_word = [
                self.__new_syllable(
                    stress=i == stress_place
                ) for i in range(random_length)
            ]
            words.append("·".join(new_word))
        return words

    def __new_syllable(self, stress=False):
        building_syllable = ""
        for i in self.syllable_struct:
            if "(" in i and ")" in i and choice((True, False)):
                continue
            i = i.replace("(", "").replace(")", "")
            building_syllable += choice(self.phonemes[i])
        return building_syllable if not stress else "ˈ"+building_syllable

    @staticmethod
    def __break_into_list(target) -> List[str]:
        import re
        optional = re.compile(r"\(?\w\)?")
        return re.findall(optional, target)


class Formatter(PhonexReader):
    def __init__(self, filename: str):
        super().__init__(filename)

    def format(self):
        pass
