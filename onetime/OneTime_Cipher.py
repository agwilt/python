#!/usr/bin/env python
# OneTime Papa Edition

from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import pickle, random
from time import time

def set_file():
	global source_file
	source_file = filedialog.askopenfilename()
	fileLabel['text'] = source_file

def onetime(text,key,n=1):
	if len(text) > 1024:
		text = text[:1024]
		simpledialog.messagebox.showwarning(title='Plaintext too long',message='WARNING: Your plaintext is longer than 1024 characters. It will now be truncated to 1024 characters.')
	output = [chr((ord(text[i]) + n * key[i]) % 256) for i in range(len(text))]
	return("".join(output))

def encrypt():
	try:
		plaintext = open(source_file).read()
	except:
		simpledialog.messagebox.showerror(title='Error',message='Warning: Please define a valid plaintext file')
	key = keys[keyName.get()]
	ciphertext = onetime(plaintext,key)
	save_file = filedialog.asksaveasfilename()	
	if save_file:
		open(save_file,'w').write(ciphertext)
	else:
		simpledialog.messagebox.showerror(title='Error',message='Invalid file name')

def decrypt():
	try:
		ciphertext = open(source_file).read()
	except:
		simpledialog.messagebox.showerror(title='Error',message='Warning: Please define a valid ciphertext file')
	key = keys[keyName.get()]
	plaintext = onetime(ciphertext,key,n=-1)
	save_file = filedialog.asksaveasfilename()
	if save_file:
		open(save_file,'w').write(plaintext)
	else:
		simpledialog.messagebox.showerror(title='Error',message='Invalid file name')

source_file = '<none>'

def init(root,getpath):
	global fileLabel, keyName, path, keys
	path = getpath
	try:
		keys = pickle.load(open(path + 'keys.p','rb'))
	except:
		filedialog.messagebox.showerror(title='Keyfile not found',message="You don't seem to have a key file :( \nPlease use <Manage> to make one")
	top = Frame(root,padx=10,pady=10)
	top.pack(expand=YES)
	fileButton = Button(top,text='File:',command=set_file)
	fileButton.grid(row=0,column=0)
	fileLabel = Label(top,text=source_file)
	fileLabel.grid(row=0,column=1)
	Label(top,text='Key:').grid(row=1,column=0)
	keyName = Spinbox(top,values=tuple(keys.keys()))
	keyName.grid(row=1,column=1)
	Button(top,text='ENCRYPT',command=encrypt).grid(row=2,column=0)
	Button(top,text='DECRYPT',command=decrypt).grid(row=2,column=1)
