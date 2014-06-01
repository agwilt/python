#!/usr/bin/env python3
# OneTime Papa Edition Main Window
# With an overview of everything:
# key manager
# en/de-crypter
# KeyGen(r) :p

from tkinter import *
from tkinter import filedialog
import random, pickle, os, sys

def keygen():
	save_file = filedialog.asksaveasfilename()
	key = [ random.randint(0,255) for x in range(1024) ]
	if save_file:
		pickle.dump(key,open(save_file,'wb'))

def cipher():
	sidewindow('OneTime_Cipher')

def manage():
	sidewindow('OneTime_Manager')

def sidewindow(thing):
	global rightbit
	global righton
	global right
	exec("import " + thing)
	if righton:
		canvas.delete(rightbit)
		right.destroy()
		righton = 0
	else:
		right = Frame(canvas, relief=GROOVE, borderwidth=2)
		rightbit = canvas.create_window(640,480,window=right,anchor=SE)
		exec(thing + ".init(right,path)")
		righton = 1

user = os.getlogin()

if sys.platform == 'darwin':
        path = '/Users/%s/.dcryptpe/' % user
elif 'lin' in sys.platform:
        path = '/home/%s/.dcryptpe/' % user
else:
        print("Error: Can't sepcify platform")
        path = str(filedialog.askdirectory() + '/.dcryptpe/')

if not os.path.isdir(path): # check for first run conditions
        os.mkdir(path)

righton = 0

root = Tk()
root.wm_title('OneTime Papa Edition')
root.resizable(0,0)
canvas = Canvas(root, width=640, height=480)
background = PhotoImage(file="/home/andreas/Programming/python/papa/background.gif")
canvas.create_image(0,0,image=background,anchor=NW)
canvas.pack()
top = Frame(canvas, relief=GROOVE, borderwidth=2)
middle = Frame(canvas, relief=GROOVE, borderwidth=2)
bottom = Frame(canvas, relief=GROOVE, borderwidth=2)
Button(top, text='KeyGen', command=keygen).pack()
Button(middle, text='Manager', command=manage).pack()
Button(bottom, text='Cipher', command=cipher).pack()
canvas.create_window(100,100,window=top,anchor=CENTER)
canvas.create_window(100,200,window=middle,anchor=CENTER)
canvas.create_window(100,300,window=bottom,anchor=CENTER)
root.mainloop()
