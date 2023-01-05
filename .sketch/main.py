from .core import SetupCL, WordGenerator

sample = SetupCL("samples/test")
gen = WordGenerator(sample)
print(gen.generate(10))
