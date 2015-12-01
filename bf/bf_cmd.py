#!/usr/bin/env python3

class BracketError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Machine():

	def __init__(self):
		self.tape = [0]
		self.p = 0

	def run(self, code):
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



if __name__ == "__main__":

	helptext = "h: Display this help text\nq: Quit\nd: Print tape, pointer\nr: Reset tape"
	tape = Machine()

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
		elif command == "r" or command == "reset":
			tape = Machine()
			print("Tape Reset.")
		else:
			tape.run(command)
	print("Goodbye!")
