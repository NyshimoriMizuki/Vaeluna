from json import loads, dumps
from typing import Dict, List


class SetupCL:
    def __init__(self, scl_file: str) -> None:
        self.syllable_struct = ""
        self.word_length = 0
        self.phonemes: Dict[str, List[str]] = dict()
        self.read_json(
            scl_file if ".scl.json" in scl_file else scl_file+".scl.json")

    def is_inicilized(self):
        if self.syllable_struct and self.word_length and self.phonemes:
            return True
        return False

    def add_phoneme(self, group: str, phoneme: str):
        if not group in self.phonemes.keys():
            raise Exception(f"Group <{group}> does not exist")
        self.phonemes[group].append(phoneme)

    def add_phonemes(self, group: str, phonemes: list[str]):
        if not group in self.phonemes.keys():
            raise Exception(f"Group <{group}> does not exist")
        for phoneme in phonemes:
            self.phonemes[group].append(phoneme)

    def read_json(self, file: str):
        with open(file, "r", encoding="utf8") as f:
            json = loads(f.read())
        for param in ["syllable_struct", "word_length", "phonemes"]:
            if not param in json.keys():
                raise Exception(f'missing "{param}" parameter on {file}')
        if type(json["phonemes"]) != dict:
            raise Exception(f'"phonemes" should be a dict')

        self.syllable_struct = json["syllable_struct"]
        self.word_length = json["word_length"]
        self.phonemes = json["phonemes"]

    def export_as_json(self, output_name):
        tmp_json = {
            "syllable_struct": self.syllable_struct,
            "word_length": self.word_length,
            "phonemes": self.phonemes
        }
        with open(output_name+".scl.json", "w", encoding="utf8") as f:
            dumps(tmp_json, f)
