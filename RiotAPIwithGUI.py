from Tkinter import *
from Dialog import *
from PIL import Image, ImageTk
from SpellCalculator import *
import os


class GUI(object):

	def __init__(self):
		self.width = 800 # Feel free to change this value!
		self.height = 500
		self.numberOfSpells = 5
		self.calculator = RiotAPIandCalculator(self.numberOfSpells)
		# Initialize defaults
		self.abilityPower = 0
		self.attackDamage = 0
		self.cooldownReduction = 0
		self.init()

	def init(self):
		self.root = Tk()
		self.canvas = Canvas(self.root, width = self.width, height = self.height, bg = "steel blue")
		self.canvas.pack()
		self.root.canvas = self.canvas.canvas = self.canvas
		self.root.bind("<Button-1>", self.onMousePressed)
		self.root.bind("<Key>", self.onKeyPressed)
		self.initFramework()
		self.root.mainloop()

	def initFramework(self):
		self.initGraphics()
		self.buttonFrame = Frame(self.root)
		self.b0 = Button(self.buttonFrame, text="Enter Stats", command=self.button0Pressed)
		self.b0.grid(row=0,column=0)
		# self.b1 = Button(self.buttonFrame, text="Calculate", command=self.button1Pressed)
		# self.b1.grid(row=0,column=1)
		self.buttonFrame.pack(side=TOP)
		self.canvas.pack()

	def initGraphics(self):
		self.bg = PhotoImage(file = "bg.gif")
		self.canvas.create_image(0,0,image=self.bg,anchor=NW)
		self.margin = self.width / 15
		self.canvas.create_text(10,0,anchor=NW, text = "Enter stats and then press enter or click OK.", font = "Helvetica 10 bold",fill = "white")
		self.canvas.create_text(10,15,anchor=NW, text = "The calculator will return the top 5 most efficient spells for those stats.", font = "Helvetica 10 bold",fill = "white")
		self.canvas.create_text(10,30,anchor=NW, text = "CDR up to 100 is valid, since the results are interesting.", font = "Helvetica 10 bold",fill = "white")
		self.canvas.create_text(10,45,anchor=NW, text = "Press r to restart.", font = "Helvetica 10 bold",fill = "white")

		self.canvas.create_text(5,self.height - 5, text = "Created by: Anthony Kuntz | Ninjasorcerer", anchor = W, font = "Helvetica 8", fill = "black")

	def onMousePressed(self, event):
		if isinstance(event.widget, Button): return
		self.canvas = event.widget.canvas

	def onKeyPressed(self, event):
		self.canvas = event.widget.canvas
		if event.keysym == "r":
			self.canvas.delete(ALL)
			self.initGraphics()

	def showDialog(self):
		dialog = MyDialog(self.canvas)
		return dialog.canvas.modalResult

	def button1Pressed(self):
		self.canvas.delete(ALL)
		self.initGraphics()

		spellList = self.calculator.calculate(self.abilityPower, self.attackDamage, self.cooldownReduction)
		print spellList
		# Might as well include console output
		self.listOfImages = []
		self.listOfSplashes = []
		self.listOfNames = []

		# Load the splash art and spell pictures into lists
		for i in range(self.numberOfSpells):
			self.listOfImages.append( ImageTk.PhotoImage(Image.open("spell" + os.sep + spellList[i][0])) )

			self.splash = Image.open("loading" + os.sep + spellList[i][1] + "_0.jpg")
			test = ImageTk.PhotoImage( self.splash )
			width = test.width()
			height = test.height()
			xRatio = (self.width / self.numberOfSpells / 1.2) * 1.0 / width
			self.splash = self.splash.resize((int(xRatio * width), int(xRatio * height)), Image.ANTIALIAS)
			self.splash = ImageTk.PhotoImage( self.splash )
			self.listOfSplashes.append( self.splash )

			self.listOfNames.append( spellList[i][2] )

		self.drawSpells()

	def drawSpells(self):
		# Draw the Splash Art
		for i in range(len(self.listOfSplashes)):
			width = 64
			image = self.listOfSplashes[i]
			increment = width + ( self.width - self.margin*2 - self.numberOfSpells * width ) / ( self.numberOfSpells - 1 )
			x0 = self.margin + increment * i + width / 2
			y1 = self.height / 2
			self.canvas.create_image( x0, y1, image = image, anchor = CENTER )

		# Draw the spell pictures
		for i in range(len(self.listOfImages)):
			image = self.listOfImages[i]
			increment = image.width() + ( self.width - self.margin*2 - self.numberOfSpells * image.width() ) / ( self.numberOfSpells - 1 )
			x0 = self.margin + increment * i
			y1 = self.height / 2
			b = 3
			self.canvas.create_rectangle( x0 - b, y1 - b - image.height(), x0 + b-1 + image.width(), y1 + b-1, fill = "white")
			self.canvas.create_image( x0, y1, image = image, anchor = SW )

		# Draw the text for the names
		for i in range(len(self.listOfImages)):
			name = self.listOfNames[i]
			increment = image.width() + ( self.width - self.margin*2 - self.numberOfSpells * image.width() ) / ( self.numberOfSpells - 1 )
			width = 64
			x = self.margin + increment * i + width / 2
			y = self.height * 3.0 / 4
			self.canvas.create_text(x, y, text = name, font = "Helvetica 15 bold", fill = "white")
		

	def button0Pressed(self):
		# Get values
		try:
			self.canvas.stats = str(self.showDialog())
			(self.abilityPower, self.attackDamage, self.cooldownReduction) = eval(self.canvas.stats)

			# Set default to zero
			if self.attackDamage == "": self.attackDamage = "0"
			if self.abilityPower == "": self.abilityPower = "0"
			if self.cooldownReduction == "": self.cooldownReduction = "0"

			# Convert
			self.abilityPower = int(self.abilityPower)
			self.attackDamage = int(self.attackDamage)
			self.cooldownReduction = int(self.cooldownReduction)

			# Prevent illegal input
			if self.cooldownReduction > 100: self.cooldownReduction = 100
			if self.attackDamage < 0: self.attackDamage = 0
			if self.abilityPower < 0: self.abilityPower = 0
			if self.cooldownReduction < 0: self.cooldownReduction = 0

			self.button1Pressed()
		except: pass
	

def main():
	gui = GUI()

main() # Opens and executes UI