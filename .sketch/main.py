from core import SetupCL, WordGenerator
from core.formatter import FormatterReader
from core.phevo import PhevoReader

sample = SetupCL("samples/test")
gen = WordGenerator(sample)

formater = FormatterReader("samples/test.fmtcl")
phevo = PhevoReader("samples/test_to_pex.phevo")
print(list(phevo.tokenize()))
