''' Import Libraries '''
from tkinter import *
import customtkinter
from tkinter import font
import json
import os
from PIL import Image, ImageTk


''' Import External Classes '''
from program_classes.user_class import user

''' App Class '''
class DCM(customtkinter.CTk):
  # class variables
  bg_colour = "#1A1A1A"

  gray_1 = "#2A2A2A"
  gray_2 = "#8f8f8f"

  blue_1 = "#195FA6"

  white_1 = "#D9D9D9"

  # init function to initialize the window
  def __init__(self):
    # intialize master screen
    super().__init__()
    self.title("G29 - MECHTRON 3K04 - DCM")
    self.geometry("1000x700")
    self.resizable(height=False, width=False)
    #self.create_login_screen()
    self.create_main_interface()
  
  # Methods for Page navigation

  def create_login_screen(self):
    self.frm_login_screen = customtkinter.CTkFrame(master=self, fg_color = DCM.bg_colour)
    self.frm_login_screen.pack(fill='both', expand=True)

    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)

    # center screen frame
    self.frm_login_box = customtkinter.CTkFrame(master=self.frm_login_screen, width=357, height=601, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Login label title
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Login", width=143, height=63, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title).place(relx=0.5, rely=0.2, anchor=CENTER)

    # sign in button
    customtkinter.CTkButton(master=self.frm_login_box, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=DCM.blue_1).place(relx = 0.5, rely = 0.7, anchor = CENTER)
    
    # uername text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_login_screen, placeholder_text="Enter Username", width=295, height=39, fg_color=DCM.white_1,
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box).place(relx = 0.5, rely=0.4, anchor=CENTER)
    

  def create_main_interface(self):
    pass
    

  # Other methods

  # Functions

''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()
