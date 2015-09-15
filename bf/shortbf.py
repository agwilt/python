#!/usr/bin/env python3

import sys

prog = open(sys.argv[1]).read()

p = pc = 0
tape = [0]
loop_stack = []

while pc < len(prog):

	if prog[pc] == '+':
		tape[p] = (tape[p] + 1) % 128
	elif prog[pc] == '-':
		tape[p] = (tape[p] - 1) % 128
	elif prog[pc] == '.':
		print(chr(tape[p]), end='')
	elif prog[pc] == ',':
		tape[p] = ord(input()[0]) % 128
	elif prog[pc] == '<':
		p -= 1
	elif prog[pc] == '>':
		if p > (len(tape)-2):
			tape.append(0)
		p += 1
	elif prog[pc] == ']':
		pc = loop_stack.pop() - 1
	elif prog[pc] == '[':
		if tape[p] == 0: # skip loop
			while prog[pc] != ']':
				pc += 1
		else:
			loop_stack.append(pc)
	pc += 1
