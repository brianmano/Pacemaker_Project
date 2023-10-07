''' Import Libraries '''
from tkinter import *
import customertkinter as ctk

''' Import External Classes '''
from program_classes.user_class import user

''' App Class '''
class DCM(ctk.CTk):
  # init function to initialize the window
  super().__init__(self):
  self.title("G29 - MECHTRON 3K04 - DCM")
  self.geometry("1000x700")
  self.resizable(height=False, width=False)

  # Variable definitions
  
  # Methods for Page navigation

  # Other methods

  # Functions

''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()
