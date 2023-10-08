''' Import Libraries '''
from tkinter import *
import customtkinter
from tkinter import font
import json
import os


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
    self.create_login_screen()
  
  # Methods for Page navigation

  def create_login_screen(self):
    self.frm_login_screen = customtkinter.CTkFrame(master=self, fg_color = DCM.bg_colour)
    self.frm_login_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_signup = customtkinter.CTkFont(family="Lexend", weight="bold",size=12)
    font_signup_underline = customtkinter.CTkFont(family="Lexend", weight="bold", underline = 1, size=12)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)

    # methods to bind and allow underline for any button, inputting font type 
    def on_enter(event, f):
      event.widget.config(font=f)
    def on_leave(event, f):
      event.widget.config(font=f)

    # center screen frame
    customtkinter.CTkFrame(master=self.frm_login_screen, width=357, height=601, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Login label title
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Login", width=143, height=63, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title, bg_color = DCM.gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)

    # sign in button
    customtkinter.CTkButton(master=self.frm_login_screen, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=DCM.blue_1, bg_color = DCM.gray_1).place(relx = 0.5, rely = 0.7, anchor = CENTER)
    
    # username text 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Username", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(relx=0.39, rely=0.357, anchor=CENTER)
    
    # username text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_login_screen, placeholder_text="Enter Username", width=295, height=39, fg_color=DCM.white_1,
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box).place(relx = 0.5, rely=0.4, anchor=CENTER)
    
    # password text 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Password", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(relx=0.39, rely=0.507, anchor=CENTER)
    
    # password text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_login_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1,
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box).place(relx = 0.5, rely=0.55, anchor=CENTER)

    # "Don't Have an Account?" label 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Don't Have an Account?", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.475, rely=0.76, anchor=CENTER)

    # sign up button
    signup_button = customtkinter.CTkButton(master=self.frm_login_screen, width=20, height=25, text="Sign Up", font=font_signup,
                                        state="normal", fg_color=DCM.gray_1, text_color=DCM.blue_1, hover_color=DCM.gray_1, bg_color=DCM.gray_1)
    signup_button.place(relx=0.575, rely=0.76, anchor=CENTER)
    signup_button.bind("<Enter>", lambda event, font=font_signup_underline: on_enter(event, font))
    signup_button.bind("<Leave>", lambda event, font=font_signup: on_leave(event, font))

    # forgot password button
    forgot_button = customtkinter.CTkButton(master=self.frm_login_screen, width = 20, height=25, text="Forgot Password?", font=font_sub_labels, 
                            state="normal", fg_color=DCM.gray_1, text_color=DCM.gray_2, hover_color = DCM.gray_1, bg_color = DCM.gray_1)
    forgot_button.place(relx=0.592, rely=0.6, anchor=CENTER)
    forgot_button.bind("<Enter>", lambda event, font=font_sub_labels_underlined: on_enter(event, font))
    forgot_button.bind("<Leave>", lambda event, font=font_sub_labels: on_leave(event, font))

    # x/10 users label 
    active_users = 0 #temporary 
    maximum_users = 10 
    customtkinter.CTkLabel(master=self.frm_login_screen, text= str(active_users) + "/" + str(maximum_users) + " Users", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)
  # Other methods
  
  # Functions

''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()
