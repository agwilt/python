#!/usr/bin/env python3

import sys

if "-o" in sys.argv:
	out_filename = sys.argv[sys.argv.index("-o")+1]
	sys.argv.pop(sys.argv.index("-o"))
	sys.argv.pop(sys.argv.index(out_filename))
	out_file = open(out_filename, mode='w')
else:
	out_file = sys.stdout

bf_code = open(sys.argv[1]).read()
tabs = 1

c_code = """#include <stdio.h>

int main()
{
	int p = 0;
	int tape[200] = {0};\n"""

for instr in bf_code:
	if instr == "+":
		c_code += tabs*"\t" + "tape[p]++;\n"
	elif instr == "-":
		c_code += tabs*"\t" + "tape[p]--;\n"
	elif instr == "<":
		c_code += tabs*"\t" + "p--;\n"
	elif instr == ">":
		c_code += tabs*"\t" + "p++;\n"
	elif instr == ".":
		c_code += tabs*"\t" + "putchar(tape[p]);\n"
	elif instr == ",":
		c_code += tabs*"\t" + "tape[p] = getchar();\n"
	elif instr == "[":
		c_code += tabs*"\t" + "while (tape[p] != 0) {\n"
		tabs += 1
	elif instr == "]":
		tabs -= 1
		c_code += tabs*"\t" + "}\n"

c_code += "}"

print(c_code, file=out_file)
