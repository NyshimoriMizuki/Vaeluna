from sys import argv

from core import SetupCL, WordGenerator
from core.phonex import Phonex

setup = SetupCL("samples/test")
gen = WordGenerator(setup)

targget = argv[1]

engine = Phonex(".\\samples\\test-formater.phex")
engine.preprocess()
# print(engine.vars)
print(engine.funcs['teste'].run(targget))


"""
group C { all-consonants }
group V { +C, all-vowels }


filter mergin_back_vowel:
 - o -> { i, e, a } / { ŋ, ɸ }_

"""
