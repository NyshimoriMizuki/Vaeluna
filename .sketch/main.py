from core.phonex2 import phonex_reader as phre
from core import SetupCL


setup = SetupCL("samples/test")

lexer = phre.PhonexLexer('''/ group C {All-Consonants}

@"start"
a -> æ
h→ʔ/!#_ or !_#
ps ks> s ts
aj -> ē
tVɽ -> t̠ɹ̠̊˔V
''')
print(lexer.tokenize())

"""
"""
