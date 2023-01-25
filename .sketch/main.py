from core.phonex2 import phonex_reader as phre
from core import SetupCL


setup = SetupCL("samples/test")

lexer = phre.PhonexLexer('''
/ group C {All-Consonants}

@"start"
a -> æ
h→ʔ/!#_ or !_#
ps ks> s ts
''', setup)
print(lexer.tokenize())
"""
<NEW_LINE>,
<EXPR>, <SPACE>, <PHONE;g>, <KEY;group>, <IDENT;C>, <SPACE>, <OPEN_SET>, <IDENT;All-Consonants>, <CLOSE_SET>, <NEW_LINE>, 
<NEW_LINE>,
<OPER;@>, <COMMENT;start>, <NEW_LINE>,
<PHONE;a>, <OPER;TO>, <OPER;TO>, <SPACE>, <PHONE;æ>, <NEW_LINE>,
<PHONE;h>, <PHONE;ʔ>, <OPER;!>, <OPER;#>, <OPER;_>, <SPACE>, <PHONE;o>, <SPACE>, <OPER;!>, <OPER;_>, <OPER;#>, <NEW_LINE>,
<PHONE;ps>, <PHONE;ks>, <SPACE>, <PHONE;s>, <PHONE;ts>, <EOF>
"""
