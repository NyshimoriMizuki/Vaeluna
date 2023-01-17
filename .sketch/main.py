from core import SetupCL, WordGenerator
from core.phevo import Phevo
from core.phonex_reader import LabelNode, PhonexNode

sample = SetupCL("samples/test")
gen = WordGenerator(sample)

phevo = Phevo("samples/test_to_pex.phevo")
print(LabelNode("filter", "no_aj", [PhonexNode(["aj"], ["ej"], ["target"])]))
