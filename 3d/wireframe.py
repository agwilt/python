#!/usr/bin/env python3

import math
import sys
import curses
from time import sleep
from copy import deepcopy
from curses import wrapper


def transform(vertex):
	# First: Cart. to polar, throw out r
	x, y, z = vertex
	angle_h = math.atan(y/x)
	angle_v = math.asin(z/math.sqrt(x**2+y**2+z**2))
	pixel_x = int((angle_h+(FOV_h/2) % (2*math.pi)) / FOV_h * Screen_x)
	pixel_y = int((angle_v+(FOV_v/2) % (2*math.pi)) / FOV_v * Screen_y)
	return [pixel_x, pixel_y]

def draw(point, screen):
	x, y = point
	if 0 <= x < Screen_x-1 and 0 < y <= Screen_y:
		screen.addstr(Screen_y-y, x, 'x')

def draw_line(p1,p2, screen):
	if p1[0] == p2[0]:
		x = p1[0]
		for y in range((min(p1[1],p2[1])+1),(max(p1[1],p2[1]))):
			if 0 <= x < Screen_x-1 and 0 < y <= Screen_y:
				screen.addstr(Screen_y-y, x, '|')
	else:
		if p1[1] == p2[1]:
			c = '-'
		elif (p1[1] - p2[1])/(p1[0] - p2[0]) > 0.5:
			c = '/'
		elif (p1[1] - p2[1])/(p1[0] - p2[0]) < -0.5:
			c = '\\'
		else:
			c = '*'
		m = (p2[1] - p1[1])/(p2[0] - p1[0])
		b = p1[1] - m*p1[0]
		def f(x):
			return m*x + b
		for x in range((min(p1[0],p2[0])+1),max(p1[0],p2[0])):
			y = int(f(x))
			r = f(x) % 1
			if 0 <= x < Screen_x-1 and 0 < y <= Screen_y:
				screen.addstr(Screen_y-y, x, c)

class Thing():
	def __init__(self, vertices, lines):
		self.vertices = vertices
		self.lines = lines
	def move(self, vector):
		for i, vertex in enumerate(self.vertices):
			for j, offset in enumerate(vector):
				self.vertices[i][j] += offset
	def moved(self, vector):
		#return Thing([[self.vertices[i][j]+m for j, m in enumerate(vector)] for i, v in enumerate(self.vertices)],self.lines,[self.centre[j]+m for j,m in enumerate(vector)])
		new_thing = deepcopy(self)
		new_thing.move(vector)
		return new_thing
	def rotate(self, point, angle):
		self.move([ -1 * x for x in point])
		for i, vertex in enumerate(self.vertices):
			old_x = vertex[0]
			old_y = vertex[1]
			old_z = vertex[2]
			self.vertices[i] = [(math.cos(angle)*old_x - math.sin(angle)*old_y),(math.sin(angle)*old_x + math.cos(angle)*old_y),old_z]
		self.move(point)
	def rotated(self, point, angle):
		new_thing = deepcopy(self)
		new_thing.rotate(point, angle)
		return new_thing
	def centre(self):
		return [sum([v[i] for v in self.vertices])/len(self.vertices) for i in range(3)]

def render(things, screen):
	for thing in things:
		points = [transform(vertex) for vertex in thing.vertices]
		for line in thing.lines:
			draw_line(points[line[0]],points[line[1]], screen)
		for point in points:
			draw(point, screen)
	screen.refresh()

def shutdown():
	curses.nocbreak()
	curses.echo()
	curses.endwin()

def setup():
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

def main(screen):
	global Screen_y
	global Screen_x
	global FOV_h
	global FOV_v

	Screen_y, Screen_x = screen.getmaxyx()

	if "-demo" in sys.argv:
		sys.argv.remove("-demo")
		demo = True
	else:
		demo = False

	if len(sys.argv) > 1:
		FOV_h = math.radians(int(sys.argv[1]))
	else:
		FOV_h = math.radians(50)
	FOV_v = FOV_h / Screen_x * Screen_y * 1.7

	cube = Thing([[4,-2,-2], [4,2,-2], [4,2,2], [4,-2,2], [8,-2,-2], [8,2,-2], [8,2,2], [8,-2,2]], [[0,1],[1,2],[2,3],[3,0], [4,5],[5,6],[6,7],[7,4], [0,4],[1,5],[2,6],[3,7]])
	car = Thing([[2,-4,0],[-2,-4,0],[-2,4,0],[2,4,0], [2,-4,1],[-2,-4,1],[-2,4,1],[2,4,1], \
	[2,-2,1],[-2,-2,1],[-2,2,1],[2,2,1], [2,-2,2],[-2,-2,2],[-2,2,2],[2,2,2]], \
	[[0,1],[1,2],[2,3],[3,0], [4,5],[5,6],[6,7],[7,4], [0,4],[1,5],[2,6],[3,7], \
	[8,9],[10,11],[12,13],[13,14],[14,15],[15,12],[8,12],[9,13],[10,14],[11,15]])
	car.move([15,0,-1])

	time = 0
	offset = [0,0,0]

	screen.timeout(13)

	while True:
		if demo:
			offset = [0,0,3 * math.cos(time/30)]
			car.rotate(car.centre(), 0.03)

		screen.clear()
		render([car.moved(offset)], screen)

		c = screen.getch()
		if c == ord('q'):
			car.rotate(car.centre(), 0.05)
		elif c == ord('e'):
			car.rotate(car.centre(), -0.05)
		elif c == ord('a'):
			car.move([0,-0.2,0])
		elif c == ord('d'):
			car.move([0,0.2,0])
		elif c == ord('w'):
			car.move([0,0,0.2])
		elif c == ord('s'):
			car.move([0,0,-0.2])
		elif c == ord('z'):
			car.move([-0.2,0,0])
		elif c == ord('x'):
			car.move([0.2,0,0])
		elif c != -1:
			break

		time += 1

	shutdown()
	exit()

if __name__ == "__main__":
	stdscr = curses.initscr()
	setup()
	main(stdscr)
