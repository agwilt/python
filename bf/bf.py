#!/usr/bin/env python3

import sys

# the --debug flag adds printed messages
if "--debug" in sys.argv:
	DEBUG = True
	sys.argv.pop(sys.argv.index("--debug"))
else:
	DEBUG = False

# read source code from file
# TODO: add stdin (pipe) or prompt
prog = open(sys.argv[1]).read()

pc = 0			# program counter (for tape)
p = 0			# brainfuck cell counter (that gets modified with +-)
tape = [0]		# brainfuck 'tape' full of cells
loop_stack = [] # a stack to keep track of all the [s and ]s

# execution loop
while pc < len(prog):

	if DEBUG:
		print("Instr:%s\nPC: %d\nCellN: %d\nCell: %d/%s\n" % (prog[pc],pc,p,tape[p],chr(tape[p])))

	instr = prog[pc]

	# increment, loop back to 0 at 128
	if instr == '+':
		tape[p] = (tape[p] + 1) % 128

	# decrement
	elif instr == '-':
		tape[p] = (tape[p] - 1) % 128

	# print current character
	elif instr == '.':
		print(chr(tape[p]), end='')

	# get character from stdin, %128 in case it's not ascii
	# if no character is given, set cell to 0
	# if string is given, use first character
	elif instr == ',':

		character = input()

		if character == '':
			if DEBUG:
				print("No character entered")
			tape[p] = 0
		else:
			if DEBUG:
				print("Character entered: %s, ascii %d" % (character,ord(character)))
			tape[p] = ord(character[0]) % 128

	# decrement pointer, trow error if at cell 0
	elif instr == '<':
		if p > 0:
			p -= 1
		else:
			print("Error: can't decrement pointer")
			exit(1)

	# increment pointer, extend cell array if necessary
	elif instr == '>':
		if p > (len(tape)-2):
			tape.append(0)
		p += 1

	# unconditionally jump back to corresponding [
	elif instr == ']':
		pc = loop_stack.pop() - 1

	# if cell is 0, skip to next ], otherwise add pc to stack and continue
	elif instr == '[':
		if tape[p] == 0: # skip loop
			while prog[pc] != ']':
				pc += 1
		else:
			loop_stack.append(pc)

	# increment program counter
	pc += 1
