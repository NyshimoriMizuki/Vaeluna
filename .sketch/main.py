from core import SetupCL, WordGenerator
from core.formatter import Reader

sample = SetupCL("samples/test")
gen = WordGenerator(sample)

formater = Reader("samples/test.fmtcl")
print(list(formater.tokenize()))
