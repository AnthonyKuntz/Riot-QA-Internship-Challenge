import tkSimpleDialog
import tkMessageBox
from Tkinter import *

# Adapted from course notes at cs.cmu.edu/~112
class MyDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		self.canvas = master
		self.canvas.modalResult = None
		Label(master, text="Ability Power").grid(row=0)
		Label(master, text="Attack Damage").grid(row=1)
		Label(master, text="Cooldown Reduction").grid(row=2)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		return self.e1 # initial focus
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		third = self.e3.get()
		self.canvas.modalResult = (first, second, third)