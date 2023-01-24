from core.phonex2 import phonex_reader as phre
from core import SetupCL


setup = SetupCL("samples/test")

lexer = phre.PhonexLexer("a > e", setup)
print(lexer.phonemes)
