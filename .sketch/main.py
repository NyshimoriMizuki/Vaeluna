from core.phonex2 import phonex_reader as phre
from core import SetupCL


setup = SetupCL("samples/test")


target = '''/ group C {all-consonants}

@"start"
a -> æ
h→ʔ/!#_ or !_#
ps ks> s ts
aj -> ē
tVɽ -> t̠ɹ̠̊˔V
'''
target2 = '''/ group C {all-consonants}

filter no-at:
 - at -> ēʔ
 - ēʔC -> ēC

filter no-t̠ɹ̠̊˔:
 - at -> ēʔ
 - ēʔC -> ēC
'''

lexer = phre.PhonexLexer(target2)
parser = phre.PhonexParser(setup, lexer.tokenize())
print(lexer.tokenize())
print(parser.agglutinate())

"""
"""
