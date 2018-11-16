
import Tkinter as tk    
import tkFont as tkfont  


from Tkinter import *
import Tkinter as tk

from PIL import Image
from PIL import ImageTk

import tkFileDialog
import tkMessageBox
import cv2
import csv
import os

class FrontPage(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")


		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for F in (StartPage, Cut, App):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame


			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		
		frame = self.frames[page_name]

		frame.tkraise()

	def quit(self):
		self.destroy()


class StartPage(tk.Frame): #not working correctly after exiting to main screen from cut or box

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="Welcome to the Homework Helper Data Labeller!", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, text="Cut a Sheet of Problems Into Single Problems",
							command=lambda: controller.show_frame("Cut")).pack()
		button2 = tk.Button(self, text="Label a Single Problem",
							command=lambda: controller.show_frame("App")).pack()
		button3 = tk.Button(self, text = "Exit Program", command = lambda: controller.quit()).pack()


class Cut(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self._createVariables(parent)
		self._createCanvas()
		self._createCanvasBinding()

	def _createVariables(self, parent): #initialize class variables
		self.parent = parent
		self.rectxstart = 0 #x0
		self.rectystart = 0 #y0
		self.rectxend = 0 #x1
		self.rectyend = 0 #Y1
		self.rectid = None
		self.move = False
		self.image = None
		self.n = ''
		self.val = 0
		self.panelA= None
		self.count = 0
		self.globalIm = None
		self.imageName = None
		self.filecount = 0
		self.image = None
		self.MainSheet = None

		
		
		

	def fileName(self, name): #save filename as variable
		self.n = self.imageName
		
		last.destroy()
		
		self.writeData()

	def getimagename(self): #get the image name to save in csv
		last = self.last = Toplevel(self)
	  
	  	self.n = self.imageName
		
		last.destroy()
		
		self.writeData()
		

		last.update()




	def openCSV(self): #open csv
		csvFile = "cutImage" + str(self.filecount) + ".csv"
		self.filew= open(csvFile, "wb+")
		self.writer = csv.writer(self.filew, quoting = csv.QUOTE_ALL)
		self.writer.writerow(['SheetName', 'x_st', 'x_end', 'y_st', 'y_end'])
		self.filecount +=1



	def writeData(self):

		self.writer.writerow([self.n, self.rectxstart,  self.rectxend,  self.rectystart,self.rectyend ])

	def exitProgram(self): #end program close csv
		self.filew.close()
		self.canvas.delete("all")
		self.lower()

	def _createCanvas(self): #create a canvas
			   
		btn2 = Button(self, text = "Save & Exit to Main Screen", command  = lambda: self.exitProgram()).pack(side ="bottom", fill = "both", expand = "yes")
	   	btn = Button(self, text = "Select an Image", command = self.select_image).pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")
		btn3=Button(self, text = "Clear all rectangles", command = self.goTo).pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")
		
		self.canvas = Canvas(self, width = 650, height = 800, bg = "white") #too large. Need entire bg to be image
		self.canvas.pack()

	def _createCanvasBinding(self): #use button clicks to create rectangle using startRect, movingRect, and endRect
		self.canvas.bind("<Button-1>", self.startRect)
		self.canvas.bind("<ButtonRelease-1>", self.stopRect)
		self.canvas.bind("<Motion>", self.movingRect)



	def startRect(self, event): #begin a rectangle
		self.move = True
		self.rectxstart = self.canvas.canvasx(event.x)
		self.rectystart = self.canvas.canvasy(event.y)


		self.rect = self.canvas.create_rectangle(self.rectxstart, self.rectystart, self.rectxstart, self.rectystart, outline = 'orange')
		self.rectid = self.canvas.find_closest(self.rectxstart, self.rectystart, halo=2)
		
		

	def movingRect(self, event): #evaluate movement
		if self.move:
			self.rectxend = self.canvas.canvasx(event.x)
			self.rectyend = self.canvas.canvasy(event.y)
			self.canvas.coords(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
			
		   

	def stopRect(self, event): #stop rectangle edge
		self.move = False
		self.rectxend = self.canvas.canvasx(event.x)
		self.rectyend = self.canvas.canvasy(event.y)
		self.canvas.coords(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
	
		check = self.createList()
		imName = self.getimagename()
		

	def createList(self):
		imList = (self.rectxstart, self.rectystart, self.rectxend, self.rectyend)

		self.CutDown(imList)

	def goTo(self):
		if self.count != 0:
			self.clearFile()

	def clearFile(self):
		
		self.filew.close()
		self.count = 0
		self.filecount = 0
		self.openCSV()
		self.canvas.delete("all")

		im =self.image
		basewidth = 650
		wpercent = (basewidth/float(im.size[0]))
		hsize = int((float(im.size[1]) *float(wpercent)))
		im = im.resize((basewidth, hsize), Image.ANTIALIAS)
		
		im = ImageTk.PhotoImage(im)

		self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image=im)
		self.canvas.pack(fill=X)

		self.panelA.configure(image = im) #configure if not empty
		self.panelA.image = im

		




	def select_image(self): #popup dialog to select image, wipe canvas
		global panelA # original image

		self.canvas.delete("all")


		csv = self.openCSV()

		path = tkFileDialog.askopenfilename() #file chooser dialog

		if len(path) > 0: #check to make sure we selected a file
			
			extenstionFilename = os.path.basename(path)
			self.MainSheet, fileExt = os.path.splitext(extenstionFilename)

			image = cv2.imread(path) #edge detector
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			

			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # change to proper channel to view in Tkinter

			image = Image.fromarray(image)
			
			basewidth = 650
			wpercent = (basewidth/float(image.size[0]))
			hsize = int((float(image.size[1]) *float(wpercent)))
			image = image.resize((basewidth, hsize), Image.ANTIALIAS)
			self.globalIm = image

			image = ImageTk.PhotoImage(image)
		   

			self.canvas.create_image(0, 0,image=image, anchor= "nw")
			self.canvas.pack(fill=X)

			if self.panelA is None: 
				self.panelA = Label(image=image) # create label for image
				self.panelA.image = image #stops image from being garbage collected
				

			else:
				self.panelA.configure(image = image) #configure if not empty
				self.panelA.image = image #update reference
	
	

	def CutDown(self, imList):

		copyIm = self.globalIm
		CutImage = copyIm.crop(imList)
		self.imageName = str(self.MainSheet) + str(self.count) + ".jpg"
		CutImage.save(self.imageName)
		self.count +=1
		

		

class App(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		self._createVariables(parent)
		self._createCanvas()
		self._createCanvasBinding()
   
	def _createVariables(self, parent): #initialize class variables
		self.parent = parent
		self.rectxstart = 0 
		self.rectystart = 0 
		self.rectxend = 0 
		self.rectyend = 0 
		self.rectid = None
		self.move = False
		self.image = None
		self.n = ''
		self.val = 0
		self.panelA= None
		self.count = 0
		self.path = None
		self.im = None
		self.numType = None
		self.MainSheet = None
		self.moveOn = 0
		self.correct = 1
		self.filecount = 0
	   	
		

		
	def openCSV(self): #open csv
		self.filecount +=1
		filename = str('datalabel_') + str(self.filecount) + str('.csv')
		self.filew= open(filename, "wb")
		self.writer = csv.writer(self.filew, quoting = csv.QUOTE_ALL)
		self.writer.writerow(['image', 'x_st', 'x_end', 'y_st', 'y_end', 'val', 'correct?', 'Val_Type'])
		self.count +=1

	def writeData(self):

		self.writer.writerow([self.MainSheet, self.rectxstart,  self.rectxend,  self.rectystart,self.rectyend,  self.val, self.correct, self.numType])

	def exitProgram(self): #end program close csv
		self.filew.close()
		self.canvas.delete("all")
		self.lower()

	def _createCanvas(self): #create a canvas
		
	   
		btn2 = Button(self, text = "Save & Exit to Main Screen", command  = lambda: self.exitProgram()).pack(side ="bottom", fill = "both", expand = "yes")
	   
		btn = Button(self, text = "Select an Image", command = self.select_image).pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")

		btn3=Button(self, text = "Clear all rectangles", command = self.goTo).pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")

		
		self.canvas = Canvas(self, width = 650, height = 800, bg = "white") #too large. Need entire bg to be image
		
		self.canvas.pack()

	def _createCanvasBinding(self): #use button clicks to create rectangle using startRect, movingRect, and endRect
		self.canvas.bind("<Button-1>", self.startRect)
		self.canvas.bind("<ButtonRelease-1>", self.stopRect)
		self.canvas.bind("<Motion>", self.movingRect)



	def startRect(self, event): #begin a rectangle
		self.move = True
		self.rectxstart = self.canvas.canvasx(event.x)
		self.rectystart = self.canvas.canvasy(event.y)


		self.rect = self.canvas.create_rectangle(self.rectxstart, self.rectystart, self.rectxstart, self.rectystart, outline = 'orange')
		self.rectid = self.canvas.find_closest(self.rectxstart, self.rectystart, halo=2)
		
		

	def movingRect(self, event): #evaluate movement
		if self.move:
			self.rectxend = self.canvas.canvasx(event.x)
			self.rectyend = self.canvas.canvasy(event.y)
			self.canvas.coords(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
			
		   

	def stopRect(self, event): #stop rectangle edge
		self.move = False
		self.rectxend = self.canvas.canvasx(event.x)
		self.rectyend = self.canvas.canvasy(event.y)
		self.canvas.coords(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
		
		#check = self.lbl() # need this to happen after image load
		

	
	def select_image(self): #popup dialog to select image, wipe canvas
		global panelA # original image

		self.canvas.delete("all")

		self.path = tkFileDialog.askopenfilename() #file chooser dialog

		csv = self.openCSV()

		if len(self.path) > 0: #check to make sure we selected a file
			self.MainSheet = os.path.basename(self.path)
			#self.MainSheet, fileExt = os.path.splitext(extenstionFilename)

			image = cv2.imread(self.path) #edge detector
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			

			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # change to proper channel to view in Tkinter

			self.im = Image.fromarray(image)
			image = self.im

			basewidth = 300
			wpercent = (basewidth/float(image.size[0]))
			hsize = int((float(image.size[1]) *float(wpercent)))
			image = image.resize((basewidth, hsize), Image.ANTIALIAS)

			image = ImageTk.PhotoImage(image)
		   

			self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image=image)
			self.canvas.pack(fill=X)

			if self.panelA is None: 
				self.panelA = Label(image=image) # create label for image
				self.panelA.image = image #stops image from being garbage collected
				

			else:
				self.panelA.configure(image = image) #configure if not empty
				self.panelA.image = image #update reference

		
		message = "Segment the first term "
		self.numType = "First Term"
		self.moveOn = 1
		self.firstTerm(message, self.numType)

	def getnum( self, info, message, numType): #return value from message box
		self.val = info.get()
	
		self.top.destroy()

		self.moveOn +=1

		exist = self.chckstate(message, numType)
	
		

	def lbl(self, message, numType): # label data
		self.nxt.destroy()
		top = self.top = Toplevel(self)
		btn = Button(top, text = "Confirm", command = lambda: self.getnum(info, message, numType))
		btn.pack(side= "bottom")

		info = Entry(top)
		info.pack()

		lab = Label(top, text = "Enter value: ")
		lab.pack()

		top.update() # or withdraw
		

		self.writeData()
		

	def chckstate(self, message, numType): #destroy toplevel
		
		nxt = self.nxt = Toplevel(self)

		msg = Message(nxt, text = "This value is: ")
		msg.pack()

		button = Button(nxt, text = "Correct", command = lambda: self.correctness(1, message, numType)).pack()
		button2 = Button(nxt, text = "Incorrect", command = lambda: self.correctness(0, message, numType)).pack()



	def correctness(self, correctness, message, numType):
		self.correct = correctness
		self.nxt.destroy()
		self.Close_Open(message, numType)

	def firstTerm(self, message, numType):
		nxt = self.nxt = Toplevel(self)
		
		msg = Message(nxt, text = message)
		msg.pack()

		nxt.type = numType

		button = Button(nxt, text = "The box was drawn correctly", command = lambda: self.lbl(message, numType)).pack() #lbl needs to call close open
		button2 = Button(nxt, text = "This value does not exist", command = lambda: self.doesNotExist(message, numType)).pack()
		button3 = Button(nxt, text = "This rectangle is drawn incorrectly" , command = lambda: self.eraseRect()).pack()


	def eraseRect(self):
		self.canvas.delete(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)


	def doesNotExist(self, message, numType):
		self.moveOn +=1
		self.Close_Open(message, numType)

	def Close_Open(self, message, numType):
		self.nxt.destroy() #not 
		self.GenerateMess(message, numType)


	def GenerateMess(self, message, numType):
		if self.moveOn ==2:

			message = "Segment the first digit in the first term" #need to be able to input 2 rectangles
			self.numType = "First Segmented First Term"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==3:
			message = "Segment the second digit in the first term"
			self.numType = "Second Segmented Second Term"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==4:
			message = "Segment the first carried number"
			self.numType = "First Carry"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==5:
			message = "Segment the second term"
			self.numType = "Second Term"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==6:
			message = "Segment the first digit in the second term"
			self.numType = "First Segmented Second Term"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==7:
			message = "Segment the second digit in the second term"
			self.numType = "Second Segmented Second Term"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==8:
			message = "Segment the second carried digit"
			self.numType = "Second Carry"

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==9:
			message = "Segment the answer"
			self.numType = "Answer"
			
			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==10:
			message = "Segment the first digit in the answer "
			self.numType = "Answer digit 1" 

			self.firstTerm(message, numType)
			self.nxt.destroy

		if self.moveOn ==11:
			message = "Segment the second digit in the answer "
			self.numType = "Answer digit 2" 

			self.firstTerm(message, numType)
			self.nxt.destroy


	def goTo(self):
		if self.count != 0:
			self.clearFile()

	def clearFile(self):
		
		self.filew.close()
		self.count = 0
		self.openCSV()
		self.canvas.delete("all")

		im =self.im
		basewidth = 300
		wpercent = (basewidth/float(im.size[0]))
		hsize = int((float(im.size[1]) *float(wpercent)))
		im = im.resize((basewidth, hsize), Image.ANTIALIAS)
		
		im = ImageTk.PhotoImage(im)

		self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image=im)
		self.canvas.pack(fill=X)

		self.panelA.configure(image = im) #configure if not empty
		self.panelA.image = im

		self.count = 0
if __name__ == "__main__":
	app = FrontPage()
	app.mainloop()
