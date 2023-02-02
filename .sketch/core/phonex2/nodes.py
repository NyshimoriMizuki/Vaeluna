from typing import Union
import re

NODE = Union['LabelNode', 'PhonexNode', "GroupNode", 'CommentNode']


class LabelNode:
    pass


class PhonexNode:
    def __init__(self, left, right, condition="_") -> None:
        self.condition = condition
        self.left = left
        self.right = right
        self.__format_values()

    def run(self, target):
        if self.in_condition(target):
            return re.sub(self.left, self.right, target)

    def in_condition(self, target):
        return re.match(self.condition, target)

    def __format_values(self):
        pass


class GroupNode:
    pass


class CommentNode:
    pass
