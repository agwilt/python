# OneTime Manager

from tkinter import *
from tkinter import filedialog, simpledialog
import pickle

def new_entry():
	global keys
	name = simpledialog.askstring('Choose Name',"Who's key is it?")
	keyfile = filedialog.askopenfilename()
	if keyfile:
		try:
			keys.update({name : pickle.load(open(keyfile,'rb'))})
		except:
			simpledialog.messagebox.showerror(title='Error',message='Error: invalid key file')
	pickle.dump(keys, open(path + 'keys.p','wb'))

def delete_entry():
	global keys
	name = NameList.get()
	if simpledialog.messagebox.askquestion(title='Delete Entry?',message='Do you really want to delete the key entry %s?' % name) == 'yes':
		keys.pop(name)
	pickle.dump(keys, open(path + 'keys.p','wb'))

def change_entry():
	global keys
	name = NameList.get()
	keyfile = filedialog.askopenfilename()
	if keyfile:
		try:
			keys[name] = pickle.load(open(keyfile,'rb'))
		except:
			simpledialog.messagebox.showerror(title='Error',message='Error: invalid key file')
	pickle.dump(keys, open(path + 'keys.p','wb'))
# begin prestart

## end prestart

def init(root,getpath):
	global NameList, path, keys
	path = getpath
	try:
		keys = pickle.load(open(path + 'keys.p','rb'))
	except:
		keys = {}
		pickle.dump(keys, open(path + 'keys.p','wb'))
	top = Frame(root,padx=10,pady=10)
	top.pack()
	NameList = Spinbox(top,values=tuple(keys.keys()))
	NameList.grid(row=0,column=0)
	Button(top,text='New',command=new_entry).grid(row=0,column=1)
	Button(top,text='Delete',command=delete_entry).grid(row=1,column=0)
	Button(top,text='Change',command=change_entry).grid(row=1,column=1)


## at end


## / at end
