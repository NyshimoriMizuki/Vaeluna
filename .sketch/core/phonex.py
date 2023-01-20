from abc import ABC, abstractmethod
import re
from typing import Dict


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


class Filter:
    def __init__(self, filter_node: 'LabelNode') -> None:
        self.phonexs = [Phonex.build_phonex(i) for i in filter_node.content]

    def __repr__(self) -> str:
        return f"Filter: {self.phonexs}"

    def run(self, target):
        for line in self.phonexs:
            for case, to in line:
                target = self.applier(
                    (case, to if not to in "0*∅" else ""), target)
        return target

    @staticmethod
    def applier(x, z):
        return re.sub(x[0], x[1], z)
    # [[<function >, <function >], [<function >, <function >]]


class Phonex:
    def __init__(self, filename: str):
        self.ast = PhonexReader(filename).tokenize().get_parsed_text()
        self.vars = dict()
        self.funcs: Dict[str, Filter] = dict()

    def run(self, targets: list):
        pass

    def preprocess(self):
        for node in self.ast:
            if type(node) == GroupNode:
                self.vars.update({
                    node.id: (node.value[0]+extend_group
                                 if (extend_group := self.__get_extend_group(node.value[-1]))
                                 else node.value[0])
                })
            elif type(node) == LabelNode and node.type == 'filter':
                self.funcs.update({node.name: Filter(node)})
            else:
                print(f"Unknown node: <{node}>")

    @staticmethod
    def build_phonex(phonex_node: 'PhonexNode'):
        # PhonemeExpression { condition: _, left: [['we']], right: [['wa']] }
        # .use(target)
        # // return re.replace(r'(we', 'wa', target):
        # //
        phonexs = []
        for group_l, group_r in zip(phonex_node.left, phonex_node.right):
            for i, v in enumerate(group_l):
                condition, around = parse_condition(
                    phonex_node.condition, target=v)
                subtitute_to = ''

                if len(group_l) >= len(group_r):
                    subtitute_to = index_in(i, group_r)

                    if around['before']:
                        subtitute_to = around['before']+subtitute_to
                    if around['after']:
                        subtitute_to += around['after']
                else:
                    for i in subtitute_to:
                        if around['before']:
                            subtitute_to[i] = around['before']+subtitute_to[i]
                        if around['after']:
                            subtitute_to[i] += around['after']

                phonexs.append(
                    (condition, subtitute_to)
                )
        return phonexs

    def __get_extend_group(self, group_name):
        if group_name != "extends:None":
            if not group_name[-1] in self.vars.keys():
                raise Exception(f"no group called <{group_name[-1]}>")
            return self.vars[group_name[-1]]


class PhonexReader:
    def __init__(self, filename: str):
        with open(filename, "r", encoding="utf8") as f:
            self.file_content = f.read()
        self.parsed_text = []

    def get_parsed_text(self):
        if self.parsed_text:
            return self.parsed_text
        raise Exception("PhonexReader is not tokenized")

    def tokenize(self):
        group = re.compile(
            r'(group|define|def)\s*(?P<name>[A-Z])\s*{\s*(?P<extend>[A-Z]\+|\+[A-Z])?\s*(?P<value>.+)\s*}')
        stopcomment = re.compile(r'@"(?P<message>.*)"')
        label = re.compile(r"^(?P<type>filter|rominize)? ?(?P<name>.+):$")
        phonex = re.compile(
            r'^(?P<indent> - |—)?(?P<left>{.+}|.+) +(->|>|→) +(?P<right>{.+}|[^\n\/]+) *(?P<case>\/.+$|$)')

        for line in self.file_content.split("\n"):
            new_match = None
            if (match := re.match(group, line)):
                match = match.groupdict() if match else match
                value = break_to_list(match["value"])
                value.append(
                    f"extends:{str(match['extend']).replace('+', '')}")
                new_match = GroupNode(match["name"], value)

            elif (match := re.match(stopcomment, line)):
                new_match = StopCommentNode(match["message"])

            elif (match := re.match(label, line)):
                new_match = LabelNode(match["type"], match["name"])

            elif (match := re.match(phonex, line)):
                phonex_node = PhonexNode(
                    break_to_list(match["left"]),
                    break_to_list(match["right"]),
                    match["case"] if match["case"] else "_"
                )

                if match["indent"] and len(self.parsed_text) > 0 and type(self.parsed_text[-1]) == LabelNode:
                    self.parsed_text[-1].add_content(phonex_node)
                    continue
                new_match = phonex_node
            else:
                new_match = UnknownNode(line)

            if line:
                self.parsed_text.append(new_match)
        return self


def parse_condition(condition: str, target: str) -> re.Pattern:
    condition = condition.replace("/ ", "").replace("/", "")

    score_index = condition.index("_")
    wb = condition.replace("#", "^") if "#_" in condition else condition
    wb = wb.replace("#", "$") if "_#" in condition else wb

    condition = condition.replace("#", "")
    return (wb.replace("_", target), {
            "before": condition[:score_index] if 0 < score_index else None,
            "after": condition[score_index+1:] if score_index+1 < len(condition) else None
            }
            )


def index_in(i: int, list_: list):
    if len(list_) < 1:
        raise Exception(f"Empty list {list_}")

    if i > len(list_):
        return list_[-1]
    return list_[i]

def break_to_list(target):
    m = []
    for i in re.split(r"{|}", target):
        if not i or i.isspace():
            continue
        m.append([i for i in re.split(r", | |,", i) if i])
    return m


def split_without_none(target: str):
    if not "{" in target:
        return list(filter(lambda x: True if x else False, target.split(" ")))
    return target


class Node(ABC):
    def __init__(self, content=None):
        self.content = content

    @ abstractmethod
    def __repr__(self) -> str:
        return f"content: {{ {self.content} }}"


class UnknownNode(Node):
    def __init__(self, content):
        self.content = content

    def __repr__(self) -> str:
        return f"Unknown {{ content: '{self.content}' }}"


class GroupNode(Node):
    def __init__(self, name: str, value: list[str]):
        self.id = name
        self.value = value

    def __repr__(self) -> str:
        return f"Group {{ id: {self.id}, value: {self.value} }}"


class PhonexNode(Node):
    def __init__(self, left: list, right: list, condition: list):
        self.left = left
        self.right = right
        self.condition = condition

    def __repr__(self) -> str:
        return f"PhonemeExpression {{ condition: {self.condition}, left: {self.left}, right: {self.right} }}"


class StopCommentNode(Node):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return f'StopComment {{ message: "{self.message} }}"'


class LabelNode(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.content = []

    def __repr__(self) -> str:
        return f"Label {{ type: {self.type}, name: {self.name}, content: {self.content} }}"

    def add_content(self, content):
        self.content.append(content)


# filter ajust_syllable:
#  - C%V -> C%ʔV
#  - C%ʔV -> {C%ʔV, %CV} / C=W
