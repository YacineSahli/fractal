from tkinter import *
import math

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Fractal")
        self.canvas = Canvas(master, width=800, height=(500))
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind("<Button-1>", self.callback)
        self.line = Line(-1, -1, -1, -1)
        self.lines = []

        self.b = Button(master, text="reset", width=30, command=self.clean)
        self.labelN = Label(master, text="Polygon")
        self.labelL = Label(master, text="Level")
        self.entryN = Entry(master,width=10)
        self.entryL = Entry(master, width=10)
        self.entryN.insert(0, 3)
        self.entryL.insert(0,2)
        self.b.pack()
        self.labelN.pack(side=LEFT, anchor=CENTER)
        self.entryN.pack(side=LEFT)
        self.labelL.pack(side=LEFT)
        self.entryL.pack(side=LEFT)

    def clean(self):
        self.canvas.delete("all")
        self.line.x1= -1

    def drawFractal(self, level):
        if(int(self.entryN.get()) < 3):
            return
        if(level <= 0):
            for line in self.lines:
                self.canvas.create_line(line.x1, line.y1, line.x2, line.y2, smooth=TRUE)
        else:
            newLines = []
            for line in self.lines:
                angle = 360 / int(self.entryN.get())
                angle = math.radians(angle) # convert from degrees to radians
                
                line1 = Line(line.x1 , line.y1 , (line.x2- line.x1) / 3+ line.x1, (line.y2-line.y1) /3 + line.y1)
                line3 = Line(2*(line.x2- line.x1) / 3+ line.x1,  2*(line.y2-line.y1) /3 + line.y1, line.x2, line.y2)
                currentAngle = -self.getAngle(line1)
                polyLines = []
                length = math.sqrt(math.pow(line1.x2-line1.x1, 2) + math.pow(line1.y2-line1.y1,2))
                polyLine = Line(line3.x1, line3.y1, line3.x2 , line3.y2)
                for i in range(int(self.entryN.get()) - 1):
                    currentAngle = currentAngle + angle
                    xMove = math.cos(currentAngle) * length
                    yMove = -math.sin(currentAngle) * length
                    polyLine = Line(polyLine.x1 + xMove, polyLine.y1  + yMove, polyLine.x1 , polyLine.y1)
                    polyLines.append(polyLine)

                newLines.append(line1)
                for polyLine in polyLines:
                    newLines.append(polyLine)
                newLines.append(line3)
            level = level -1
            self.lines = newLines
            self.drawFractal(level)

    def callback(self, event):
        if( self.line.x1 == -1):
            self.line.x1 = event.x
            self.line.y1 = event.y
        elif( self.line.x2 == -1):
            self.line.x2 = event.x
            self.line.y2 = event.y
            self.lines.append(self.line)
            self.drawFractal(int(self.entryL.get()))
            self.line = Line(-1, -1, -1, -1)
            self.lines= []
        

    def getAngle(self, line):
        xDiff = line.x2 - line.x1
        yDiff = line.y2 - line.y1
        return math.atan2(yDiff, xDiff)
        
root = Tk()
gui = GUI(root)
root.mainloop()