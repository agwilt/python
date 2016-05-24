#!/usr/bin/env python3

import string

class BracketError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Machine():

	def __init__(self):
		self.tape = [0]
		self.p = 0

	def run(self, code, step=False):
		pc = 0
		loop_stack = []
		brackets = 0
		printed = False

		for instr in code:
			if instr == '[':
				brackets += 1
			elif instr == ']':
				brackets -= 1
		if brackets != 0:
			raise BracketError('Error: failed bracket count')

		while pc < len(code):
			instr = code[pc]
			# increment/decrement
			if instr == '+':
				self.increment(1)
			elif instr == '-':
				self.increment(-1)
			# I/O
			elif instr == '.':
				print(chr(self.cell()), end='')
				printed = True
			elif instr == ',':
				self.input()
			# move tape
			elif instr == '<':
				if self.p > 0:
					self.p -= 1
				else:
					print("Error: Can't decrement pointer")
			elif instr == '>':
				if self.p > (len(self.tape)-2):
					self.tape.append(0)
				self.p += 1
			# looping
			elif instr == ']':
				pc = loop_stack.pop() - 1
			elif instr == '[':
				if self.cell() == 0:
					while code[pc] != ']':
						pc += 1
				else:
					loop_stack.append(pc)

			if step:
				input()
			pc += 1
		if printed:
			print('')

	def set(self, val):
		self.tape[self.p] = val % 128

	def increment(self, amount):
		self.set(self.cell() + amount)

	def input(self):
		character = input()
		if character == '':
			print("No value given, setting cell to 0 ...")
			self.set(0)
		else:
			self.set(ord(character[0]))

	def cell(self):
		return self.tape[self.p]

	def dump(self):
		print("%d," % self.p, self.tape)


def write_to(program, command):
	split = command.index(' ')
	line = int(command[:split])
	command = command[(split+1):]
	if line < len(program):
		program[line] = command
	else:
		while len(program) < line:
			program.append('')
		program.append(command)

if __name__ == "__main__":

	helptext = "help: Display this help text\nquit: Quit\ndump: Print tape, pointer\nclear: Reset tape\nnew: Wipe program\nlist: List program\nrun: Run program\nsave <arg>: Save program as <arg>\nload <arg>: Load program from <arg>\nstep [arg]: step through program or optional arg"
	tape = Machine()
	program = []

	while True:
		try:
			command = input("[%d]:%d$ " %(tape.p,tape.cell()))
		except EOFError:
			break
		if command == "":
			continue
		elif command == "q" or command == "quit":
			break
		elif command == "d" or command == "dump":
			tape.dump()
		elif command == "h" or command == "help":
			print(helptext)
		elif command == "new":
			program = []
		elif command == "clear":
			tape = Machine()
			print("Tape Reset")
		elif command == "l" or command == "list":
			for number, line in enumerate(program):
				if line != '':
					print(number, line)
		elif command == "r" or command == "run":
			tape.run("".join(program))
		elif command[:4] == "load":
			f = open(command[5:],mode='r')
			program = f.read().split('\n')
			f.close()
		elif command[:4] == "save":
			f = open(command[5:],mode='w')
			f.write('\n'.join(program))
			f.close()
		elif command == "step":
			tape.run(program, step=True)
		elif command[:4] == "step":
			tape.run(command[5:], step=True)
		elif command[0] in string.digits:
			write_to(program, command)
		else:
			try:
				tape.run(command)
			except BracketError:
				print("Error: Failed bracket count!")
	print("Goodbye!")
