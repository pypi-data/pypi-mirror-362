import time
import tkinter as tk



class WASDHandler(tk.Frame):
    def __init__(self, parent, pycoordHandle):
        self.pycoordHandle = pycoordHandle
        tk.Frame.__init__(self, parent, width=400,  height=400)

        self.steps = tk.IntVar(value=1)
        self.speed = tk.IntVar(value=1)   

        tk.Label(self, text="Steps:").pack()
        tk.Entry(self, textvariable=self.steps).pack()
        tk.Label(self, text="Speed:").pack()
        tk.Entry(self, textvariable=self.speed).pack()     

        self.label = tk.Label(self, text="Press WASD to move! ", width=20)
        self.label.pack(fill="both", padx=50, pady=50)

        

        self.label.bind("<w>", self.onW)
        self.label.bind("<a>", self.onA)
        self.label.bind("<s>", self.onS)
        self.label.bind("<d>", self.onD)
        self.label.bind("<e>", self.onE)
        self.label.bind("<c>", self.onC)
        self.label.bind("<Return>", self.onEnter)

        # give keyboard focus to the label by default, and whenever
        # the user clicks on it
        self.label.focus_set()
        self.label.bind("<1>", lambda event: self.label.focus_set())

    def onW(self, event):
        self.pycoordHandle.relativePos(x=[self.steps.get(),self.speed.get()])

    def onA(self, event):
        self.pycoordHandle.relativePos(y=[-self.steps.get(),self.speed.get()])

    def onS(self, event):
        self.pycoordHandle.relativePos(x=[-self.steps.get(),self.speed.get()])

    def onD(self, event):       
        self.pycoordHandle.relativePos(y=[self.steps.get(),self.speed.get()])

    def onE(self, event):
        self.pycoordHandle.relativePos(z=[self.steps.get(),self.speed.get()])
    
    def onC(self, event):
        self.pycoordHandle.relativePos(z=[-self.steps.get(),self.speed.get()])

    def onEnter(self, event):
        print("Enter")
        self.pycoordHandle.measurement_positions.append(self.pycoordHandle.getPos())
           

