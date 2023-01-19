from core import SetupCL, WordGenerator
from core.phonex import Phonex

setup = SetupCL("samples/test")
gen = WordGenerator(setup)

engine = Phonex(".\\samples\\test-formater.phex")
engine.run()
print(engine.vars)
