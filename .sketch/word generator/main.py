import setupcl
import wordgen

sample = setupcl.SetupCL("test")
gen = wordgen.WordGenerator(sample)
print(gen.generate(10))
