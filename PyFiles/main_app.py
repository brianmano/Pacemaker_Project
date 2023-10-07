''' Import Libraries '''
from tkinter import *
import customtkinter as ctk
import json
import os

''' Import External Classes '''
from program_classes.user_class import user

''' App Class '''
class DCM(ctk.CTk):
  # init function to initialize the window
  def __init__(self):
    # intialize master screen
    super().__init__()
    self.title("G29 - MECHTRON 3K04 - DCM")
    self.geometry("1000x700")
    self.resizable(height=False, width=False)
    self.create_login_screen()

    # Variable definitions
    self.bg_colour = "#1A1A1A"
    self.gray_1 = "#2A2A2A"
    self.blue_1 = "#195FA6"
  
  # Methods for Page navigation

  def create_login_screen(self):
    self.login_frame = ctk.CTkFrame(master=self, fg_color=self.bg_colour)
  # Other methods

  # Functions

''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()
