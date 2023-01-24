from core.phonex2 import phonex_reader as phre
from core import SetupCL


setup = SetupCL("samples/test")

lexer = phre.PhonexLexer("Group C {}\na -> ʔ", setup)
print(lexer.src, lexer.tokenize(), sep="\n\n")
