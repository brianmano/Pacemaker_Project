from tkinter import *


class MainWindow(Tk):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.test = Test(self) # test class import

        self.outputLbl = Label(self) # output Label 
        self.outputLbl.pack(side="top", fill="x", ipady=20)


class Test(Frame):
    def __init__(self, parent):
        super(Test, self).__init__()
        self.parent = parent # you can use this way to call between classes

        self._input = Entry(self.parent) 
        self._input.pack()
        self._input.bind("<Return>", self.outputMW)

    def outputMW(self, event):  # function, when pressing return it gives changes the text in your label
        var = self._input.get()
        self.parent.outputLbl.config(text=var)  # self.parent makes the reference to your other class


if __name__ == '__main__':
    mw = MainWindow()
    mw.geometry("500x500")
    mw.mainloop()