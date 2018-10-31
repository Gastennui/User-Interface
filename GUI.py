
import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2


from Tkinter import *
import Tkinter as tk

from PIL import Image
from PIL import ImageTk

import tkFileDialog
import tkMessageBox
import cv2
import csv

class SampleApp(tk.Tk):

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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Homework Helper Data Labeller!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Cut a Sheet of Problems Into Single Problems",
                            command=lambda: controller.show_frame("Cut"))
        button2 = tk.Button(self, text="Label a Single Problem",
                            command=lambda: controller.show_frame("App"))
        button1.pack()
        button2.pack()


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
        
        
        csv = self.openCSV() #NEED TO FIND WAY TO NAME IMAGES CONSEC

    def fileName(self, name): #save filename as variable
        self.n = name.get()
        
        self.last.destroy()
        
        self.writeData()

    def getimagename(self): #SEND THIS TO UPLOAD
        last = self.last = Toplevel(self)
      
        name = Entry(last)
        name.pack()

        lab = Label(last, text = "Enter sheet name: ")
        lab.pack()

        

        btn = Button(last, text = "Confirm", command = lambda: self.fileName(name))
        btn.pack()
      
        last.update()
        
    def openCSV(self): #open csv
        self.filew= open('individualImgLoc.csv', "wb")
        self.writer = csv.writer(self.filew, quoting = csv.QUOTE_ALL)
        self.writer.writerow(['SheetName', 'x_st', 'x_end', 'y_st', 'y_end'])

    def writeData(self):

        self.writer.writerow([self.n, self.rectxstart,  self.rectxend,  self.rectystart,self.rectyend ])

    def exitProgram(self): #end program close csv
        self.filew.close()

        self.destroy()

    def _createCanvas(self): #create a canvas
               
        btn2 = Button(self, text = "Save & Exit to Main Screen", command  = lambda: self.exitProgram()).pack(side ="bottom", fill = "both", expand = "yes")
        btn = Button(self, text = "Select an Image", command = self.select_image)
        btn.pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")
        #btn3 = Button(self, text = "All Math Problems Highlighted. Cut into Single Problem", command = lambda: self.getimagename()).pack(side = "bottom", fill = "both", expand = "yes")
        
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
        check = self.keep_rect()
    def createList(self):
        imList = (self.rectxstart, self.rectystart, self.rectxend, self.rectyend)

        self.CutDown(imList)
        #imList(self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
        #self.imageList.append(imList)


    def keep_rect(self): #keep or destroy rectangle drawn
        
        MsgBox= tkMessageBox.askquestion('Rectangle created', 'Keep rectangle?', icon = None)
      
        if MsgBox == 'no':
            
            self.canvas.delete(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
        if MsgBox == 'yes':
            
            lab = self.createList()
            self.getimagename()
    def select_image(self): #popup dialog to select image, wipe canvas
        global panelA # original image

        self.canvas.delete("all")

        path = tkFileDialog.askopenfilename() #file chooser dialog

        if len(path) > 0: #check to make sure we selected a file
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
        imageName = "cutImage" + str(self.count) + ".jpg"
        CutImage.save(imageName)
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
       
        
        csv = self.openCSV()

    def fileName(self, name): #save filename as variable
        self.n = name.get()
        
        self.last.destroy()
        self.writeData()

    def getimagename(self): #get the image name to save in csv
        last = self.last = Toplevel(self)
      
        name = Entry(last)
        name.pack()

        lab = Label(last, text = "Enter image name: ")
        lab.pack()

        

        btn = Button(last, text = "Confirm", command = lambda: self.fileName(name))
        btn.pack()
      
        last.update()
        
    def openCSV(self): #open csv
        self.filew= open('dataLabels.csv', "wb")
        self.writer = csv.writer(self.filew, quoting = csv.QUOTE_ALL)
        self.writer.writerow(['image', 'x_st', 'x_end', 'y_st', 'y_end', 'val', 'single_dig', 'final_answer', 'carried', 'nonsense', 'neither', 'correct', 'incorrect'])

    def writeData(self):

        self.writer.writerow([self.n, self.rectxstart,  self.rectxend,  self.rectystart,self.rectyend,  self.val,  self.nxt.dig.get(),  self.nxt.fullNum.get(), self.nxt.carry.get(),self.nxt.nonesense.get(),  self.nxt.neither.get(),  self.nxt.correct.get(),  self.nxt.incorrect.get() ])

    def exitProgram(self): #end program close csv
        self.filew.close()

        self.destroy()

    def _createCanvas(self): #create a canvas
        
       
        btn2 = Button(self, text = "Save & Exit to Main Screen", command  = lambda: self.exitProgram()).pack(side ="bottom", fill = "both", expand = "yes")
       
        btn = Button(self, text = "Select an Image", command = self.select_image)
        btn.pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady="10")


        
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
        check = self.keep_rect()

    def keep_rect(self): #keep or destroy rectangle drawn
        
        MsgBox= tkMessageBox.askquestion('Rectangle created', 'Keep rectangle?', icon = None)
      
        if MsgBox == 'no':
            
            self.canvas.delete(self.rectid, self.rectxstart, self.rectystart, self.rectxend, self.rectyend)
        if MsgBox == 'yes':
            
            lab = self.lbl() # change so that this just calls a function that records each rectangle, then pass rectangle and crop

    def select_image(self): #popup dialog to select image, wipe canvas
        global panelA # original image

        self.canvas.delete("all")

        path = tkFileDialog.askopenfilename() #file chooser dialog

        if len(path) > 0: #check to make sure we selected a file
            image = cv2.imread(path) #edge detector
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # change to proper channel to view in Tkinter

            image = Image.fromarray(image)

            basewidth = 650
            wpercent = (basewidth/float(image.size[0]))
            hsize = int((float(image.size[1]) *float(wpercent)))
            image = image.resize((basewidth, hsize), Image.ANTIALIAS)

            image = ImageTk.PhotoImage(image)
           

            self.canvas.create_image(400, 200,image=image)
            self.canvas.pack(fill=X)

            if self.panelA is None: 
                self.panelA = Label(image=image) # create label for image
                self.panelA.image = image #stops image from being garbage collected
                

            else:
                self.panelA.configure(image = image) #configure if not empty
                self.panelA.image = image #update reference
    def getnum( self, info): #return value from message box
        self.val = info.get()
    
        self.top.destroy()

        chk = self.checklist()

    def lbl(self): # label data
        
        top = self.top = Toplevel(self)
        btn = Button(top, text = "Confirm", command = lambda: self.getnum(info))
        btn.pack(side= "bottom")

        info = Entry(top)
        info.pack()

        lab = Label(top, text = "Enter value: ")
        lab.pack()

        top.update() # or withdraw

    def chckstate(self): #destroy toplevel
        
        self.nxt.destroy()
        
        self.getimagename()
    def checklist(self): #create checklist
        
        nxt = self.nxt = Toplevel(self)

        nxt.dig = IntVar() #single digit (can also be full num, correct, incorrect)
        nxt.fullNum = IntVar() #final answer (can also be dig, correct, incorrect)
        nxt.carry = IntVar() #carried  (can also be correct, incorrect)
        nxt.correct = IntVar() #correctly done (can also be dig, full num, carry)
        nxt.incorrect = IntVar() #incorrectly done (can also be dig, full num, carry)
        nxt.nonesense = IntVar()
        nxt.neither = IntVar()


        lab=Label(nxt, text = "This value is: ")
        lab.pack()

        Checkbutton(nxt, text = 'Single Digit', variable = nxt.dig).pack()
        Checkbutton(nxt, text = 'Final Answer', variable = nxt.fullNum).pack()
        Checkbutton(nxt, text = 'Carried Number', variable = nxt.carry).pack()
        Checkbutton(nxt, text = 'Nonsense', variable = nxt.nonesense).pack()        
        Checkbutton(nxt, text = 'Correct', variable = nxt.correct).pack()
        Checkbutton(nxt, text = 'Incorrect', variable = nxt.incorrect).pack()
        Checkbutton(nxt, text = 'Neither Correct Nor Incorrect', variable = nxt.neither).pack()

        Button(nxt, text = 'Save', command = lambda: self.chckstate()).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()