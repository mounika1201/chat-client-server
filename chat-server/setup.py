import subprocess
import sys
import os


def install(package, paa):
	os.system("{} install {}".format(package, paa))


file = open("requirements.txt")

lines = file.readlines()
for line in lines:
	install(sys.argv[2], line.strip())
