''' Import Libraries '''
from tkinter import *
import customtkinter
from tkinter import font
import json
import os
import numpy as np
#from PIL import ImageTk
#import ctypes


''' Import External Classes '''
from program_classes.user_class import user


''' Global Variables for use '''
lst_parameters = ['Lower Rate Limit', 'Upper Rate Limit', 'Maximum Sensor Rate', 'Fixed AV Delay', 'Dynamic AV Delay', 'Sensed AV Delay Offset',
                  'Atrial Amplitude', 'Ventricular Amplitude', 'Atrial Pulse Width', 'Ventricular Pulse Width', 'Atrial Sensitivity', 'Ventricular Sensitivity',
                  'VRP', 'ARP', 'PVARP', 'PVARP Extension', 'Hysteresis', 'Rate Smoothing', 'ATR Duration', 'ATR Fallback Mode', 'ATR Fallback Time',
                  'Activity Threshold', 'Reaction Time', 'Response Factor', 'Recovery Time']

dict_param_nom_vals = {'Lower Rate Limit' : 60, 'Upper Rate Limit' : 120, 'Maximum Sensor Rate' : 120, 'Fixed AV Delay' : 150, 'Dynamic AV Delay' : 'Off', 'Sensed AV Delay Offset' : 'Off',
                  'Atrial Amplitude' : 3.5, 'Ventricular Amplitude' : 3.5, 'Atrial Pulse Width' : 0.4, 'Ventricular Pulse Width' : 0.4, 'Atrial Sensitivity' : 0.75, 'Ventricular Sensitivity' : 2.5,
                  'VRP' : 320, 'ARP' : 250, 'PVARP' : 250, 'PVARP Extension' : 'Off', 'Hysteresis' : 'Off', 'Rate Smoothing' : 'Off', 'ATR Duration' : 20, 'ATR Fallback Mode' : 'Off', 'ATR Fallback Time' : 1,
                  'Activity Threshold' : 'Med', 'Reaction Time' : 30, 'Response Factor' : 8, 'Recovery Time' : 5}

# dicitonary of parameters and their values and units
dict_param_and_range = {
  'Lower Rate Limit' : [[i for i in range(30, 50, 5)] + [i for i in range(50, 91, 1)] + [i for i in range(95, 180, 5)], "ppm"], # [30,35,40,45,50,51,51,...]
  'Upper Rate Limit' : [[i for i in range(50, 180, 5)], "ppm"], # [50,55,60,65,...]
  'Atrial Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.5,3.3,0.1)] + [round(i,1) for i in np.arange(3.5,7.5,0.5)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Ventricular Amplitude' : [["Off"] + [round(i,1) for i in np.arange(0.5,3.3,0.1)] + [round(i,1) for i in np.arange(3.5,7.5,0.5)], "V"], # ["Off", 0.5,0.6,0.7,0.8,...]
  'Atrial Pulse Width' : [[0.05] + [round(i,1) for i in np.arange(0.1, 2.0, 0.1)], "ms"], # [[0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
  'Ventricular Pulse Width' : [[0.05] + [round(i,1) for i in np.arange(0.1, 2.0, 0.1)], "ms"],
  'VRP' : [[i for i in range(150, 510, 10)], "ms"], # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
  'ARP' : [[i for i in range(150, 510, 10)], "ms"], # [[150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 
}

dict_modes = {'AOO' : [0, 1, 6, 8], 'VOO' : [0, 1, 7, 9], 'AAI' : [0, 1, 6, 8, 13], 'VVI' : [0, 1, 7, 9, 12]} # all current modes implemented modes and their paramaters




''' App Class '''
# class for the popup window
class credential_prompt(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.geometry("400x200")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=15)
    self.label = customtkinter.CTkLabel(self, text="Incorrect Username and/or Password",font=font)
    self.label.pack(padx=20, pady=20)

#class for admin login
class admin_login(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.geometry("400x600")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend Bold", size=40)
    self.label = customtkinter.CTkLabel(self, text="Admin Login",font=font)
    self.label.pack(padx=20, pady=20)
    #fonts
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=40)
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    # center screen frame
    customtkinter.CTkFrame(master=self, width=357, height=561, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Admin Login label title
    customtkinter.CTkLabel(master=self, text="Admin Login", width=257, height=50, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title, bg_color = DCM.gray_1).place(x=70, y=54)
    # password text 
    customtkinter.CTkLabel(master=self, text="Admin Password", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=50, y=337)
    #customtkinter.CTkLabel(master=self, text="Password", width=295, height=64, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=31, y=337)
    txtbx_password = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1).place(x=50, y=362)
    #txtbx_password.place(x = 40, y=362)
    # sign in button
    Admin_Password = "coffee" 
    customtkinter.CTkButton(master=self, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=DCM.blue_1, bg_color = DCM.gray_1, command=Admin_Password).place(x = 100, y=459)


# class for a scrollable frame in main interface
class scroll_parameters_frame(customtkinter.CTkScrollableFrame):
  def __init__(self, master, current_mode_data = None, current_mode = None, **kwargs):
    super().__init__(master, **kwargs)

    # font
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=18)
    self.current_mode_data = current_mode_data

    # checks if a mode is actually sleected, will be none when the main interface is first launched
    if current_mode != None:
      self.parameter_sliders = [customtkinter.CTkSlider(master=self, progress_color=DCM.blue_1) for i in range(len(current_mode_data))] # make a list of obj for sliders based on how many parameters
      self.parameter_values_label = [customtkinter.CTkLabel(master=self, font=font) for i in range(len(current_mode_data))] # make a list of obj for labels based on how many parameters

      # slider even to change the number displayed on the label
      def slider_event(value, index, parameter):
        self.parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][int(value)]} {dict_param_and_range[parameter][1]}' if not isinstance(dict_param_and_range[parameter][0][int(value)],str) else f'{dict_param_and_range[parameter][0][int(value)]}')

      # iterate through the all the parameters needed and makes the corresponding widgets
      for index, parameter in enumerate(current_mode_data):
        customtkinter.CTkLabel(master=self, text=parameter, font=font).grid(row=index, column=0, padx=30, pady=20)

        self.parameter_sliders[index].configure(from_=0, to=len(dict_param_and_range[parameter][0])-1, number_of_steps=len(dict_param_and_range[parameter][0]),
                                      command=lambda value=self.parameter_sliders[index].get(), index=index, parameter=parameter: slider_event(value,index,parameter))
        self.parameter_sliders[index].grid(row=index, column=1, columnspan=3, padx=30, pady=20)
        self.parameter_sliders[index].set(dict_param_and_range[parameter][0].index(current_mode_data[parameter]))
    
        self.parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][dict_param_and_range[parameter][0].index(current_mode_data[parameter])]} {dict_param_and_range[parameter][1]}' if not isinstance(current_mode_data[parameter],str) else f'{current_mode_data[parameter]}')
        self.parameter_values_label[index].grid(row=index, column=5, padx=30, pady=20)

  def get_all_values(self):
    updated_values = []
    for parameter, slider in zip(self.current_mode_data, self.parameter_sliders):
      value = dict_param_and_range[parameter][0][int(slider.get())]
      updated_values.append(value)
    return updated_values
  

# Main app classs
class DCM(customtkinter.CTk):
  # class variables
  bg_colour = "#1A1A1A"

  gray_1 = "#2A2A2A"
  gray_2 = "#8f8f8f"
  gray_3 = "#888888"

  blue_1 = "#195FA6"
  blue_2 = "#225e9c"
  blue_3 = "#317ac4"

  white_1 = "#D9D9D9"

  green_1 = "#3FAB4A"
  green_2 = "#67AB6E"

  red_1 = "#D13434"
  red_2 = "#D25E5E"

  # root file dir
  root_dir = 'user_data'

  ''' Constructor Method '''
  def __init__(self):
    # intialize master screen
    super().__init__()
    # if doesnt work on mac, get rid of these 4 lines
    #img = ImageTk.PhotoImage(file="icons/pacemaker_logo.png") 
    #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("a")
    #self.wm_iconbitmap()
    #self.iconphoto(False,img)
    # up to here and the import PIL and ctyles
    self.title("G29 - MECHTRON 3K04 - DCM")
    self.geometry("1000x700")
    self.resizable(height=False, width=False)
    self.create_login_screen()
    self.toplevel_window = None
  
  ''' Methods for page navigation '''
  # login screen
  def create_login_screen(self):
    # get all users

    lst_all_cur_users = self.get_current_users(DCM.root_dir)

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

    # center screen frame
    customtkinter.CTkFrame(master=self.frm_login_screen, width=357, height=601, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Login label title
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Login", width=143, height=63, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title, bg_color = DCM.gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)
    
    # username text 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Username or Email", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=235)
    
    # username text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_login_screen, placeholder_text="Enter Username or Email", width=295, height=39, fg_color=DCM.white_1, 
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_username.place(relx = 0.5, rely=0.4, anchor=CENTER)
    
    # password text 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Password", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=340)
    
    # password text box
    self.txtbx_password = customtkinter.CTkEntry(master=self.frm_login_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_password.place(relx = 0.5, rely=0.55, anchor=CENTER)


    # sign in button
    customtkinter.CTkButton(master=self.frm_login_screen, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=DCM.blue_1, bg_color = DCM.gray_1, command = lambda:self.attempt_login(self.txtbx_username.get(), self.txtbx_password.get(), lst_all_cur_users)).place(relx = 0.5, rely = 0.7, anchor = CENTER)

    # function to check if the key press was the enter or return key and will do the same action as pressing sign in button
    def keypress(event): 
      if event.keysym == "Return":
        self.attempt_login(self.txtbx_username.get(), self.txtbx_password.get(), lst_all_cur_users)

    # watch for keystrokes
    self.bind("<Key>", keypress)

    # "Don't Have an Account?" label 
    customtkinter.CTkLabel(master=self.frm_login_screen, text="Don't Have an Account?", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.475, rely=0.76, anchor=CENTER)

    # sign up button
    signup_button = customtkinter.CTkButton(master=self.frm_login_screen, width=20, height=25, text="Sign Up", font=font_signup,
                                        state="normal", fg_color=DCM.gray_1, text_color=DCM.blue_1, hover_color=DCM.gray_1, bg_color=DCM.gray_1, command=self.create_signup_screen)
    signup_button.place(relx=0.575, rely=0.76, anchor=CENTER)
    signup_button.bind("<Enter>", lambda e: signup_button.configure(font=font_signup_underline))
    signup_button.bind("<Leave>", lambda e: signup_button.configure(font=font_signup))

    # forgot password button
    forgot_button = customtkinter.CTkButton(master=self.frm_login_screen, width = 20, height=25, text="Forgot Password?", font=font_sub_labels, 
                            state="normal", fg_color=DCM.gray_1, text_color=DCM.gray_2, hover_color = DCM.gray_1, bg_color = DCM.gray_1)
    forgot_button.place(relx=0.592, rely=0.6, anchor=CENTER)
    forgot_button.bind("<Enter>", lambda e: forgot_button.configure(font=font_sub_labels_underlined))
    forgot_button.bind("<Leave>", lambda e: forgot_button.configure(font=font_sub_labels))

    # x/10 users label 
    active_users = len(lst_all_cur_users[0])
    maximum_users = 10 
    customtkinter.CTkLabel(master=self.frm_login_screen, text=f"{active_users}/{maximum_users} Users", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)
  
  # main interface
  def create_main_interface(self, current_user):
    for widget in self.winfo_children():
      widget.pack_forget()

    #fonts
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_username = customtkinter.CTkFont(family="Lexend", weight="bold",size=35)
    font_sections = customtkinter.CTkFont(family="Lexend", weight="bold",size=24)
    font_curmode = customtkinter.CTkFont(family="Lexend", size=20)
    font_connect = customtkinter.CTkFont(family="Lexend", size=15)

    #frame
    self.frm_main_interface = customtkinter.CTkFrame(master=self, fg_color = DCM.bg_colour)
    self.frm_main_interface.pack(fill='both', expand=True)
   
    #admin button
    customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=43, text="Admin", state="normal", font=font_buttons, fg_color=DCM.blue_1, command=self.open_admin_login).place(x = 22, y = 306)
    #run button 
    customtkinter.CTkButton(master=self.frm_main_interface, width = 117, height=43, text="Run", state="disabled", font=font_buttons, fg_color=DCM.green_1, hover_color=DCM.green_2).place(x = 22, y = 368)
    #stop button 
    customtkinter.CTkButton(master=self.frm_main_interface, width = 117, height=43, text="Stop", state="disabled", font=font_buttons, fg_color=DCM.red_1, hover_color=DCM.red_2).place(x = 159, y = 368)
    #sign out button 
    customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=43, text="Sign Out", state="normal", font=font_buttons, fg_color=DCM.blue_1, command=self.back_to_login).place(x = 22, y = 546)
    #delete account button 
    customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=33, text="Delete Account", state="disabled", font=font_buttons, fg_color=DCM.red_1, hover_color=DCM.red_2).place(x = 22, y = 603)
  
    #text for permissions
    customtkinter.CTkLabel(master=self.frm_main_interface, text="Permission: Client", width=143, height=34, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_buttons).place(x=22, y=651)
    #text for permissions
    customtkinter.CTkLabel(master=self.frm_main_interface, text=f'{current_user.get_username()}', width=199, height=40, fg_color=DCM.bg_colour, text_color=DCM.white_1, font=font_username).place(x=22, y=49)
    #text for mode
    customtkinter.CTkLabel(master=self.frm_main_interface, text="Mode", width=67, height=30, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_sections).place(x=22, y=104)
    #text for current mode
    customtkinter.CTkLabel(master=self.frm_main_interface, text=f"Current Mode: {current_user.get_current_mode()}", width=200, height=15, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_curmode).place(x=22, y=188)
    #text for parameters
    customtkinter.CTkLabel(master=self.frm_main_interface, text="Parameters", width=142, height=30, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_sections).place(x=300, y=49)
  
    #text for connected
    customtkinter.CTkLabel(master=self.frm_main_interface, text="⦿ Connected", width=154, height=34, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_connect).place(x=5, y=9)

    ''' Code for the scrollable frame and the items in it for each parameter '''
    self.frm_scroll_parameters = scroll_parameters_frame(master=self.frm_main_interface, width=665, height=585, fg_color=DCM.gray_1)
    self.frm_scroll_parameters.place(x=303,y=92)

    # dropdown menu for modes
    def load_parameters_from_mode(choice):
      dict_mode_parameters_for_user = current_user.get_all_mode_data()
      self.frm_scroll_parameters = scroll_parameters_frame(master=self.frm_main_interface, width=665, height=585, fg_color=DCM.gray_1, current_mode=choice, current_mode_data=dict_mode_parameters_for_user[choice])
      self.frm_scroll_parameters.place(x=303,y=92)

    str_default_text_mode = StringVar(value="Select a Mode")
    available_modes = [mode for mode in dict_modes]
    self.combobox_select_mode = customtkinter.CTkOptionMenu(master=self.frm_main_interface, values=available_modes, width=252, height=43, font=font_buttons, anchor="center",dynamic_resizing=True, command=load_parameters_from_mode,
                                                            dropdown_font=font_connect, fg_color=DCM.blue_1, dropdown_fg_color=DCM.blue_2, dropdown_hover_color=DCM.blue_3, corner_radius=15, bg_color=DCM.bg_colour, variable=str_default_text_mode)
    self.combobox_select_mode.place(x=23,y=147)

    
  # navigate back to log in screen
  def back_to_login(self):
    for widget in self.winfo_children():
      widget.pack_forget()
    self.create_login_screen()
  
  # register an account page
  def create_signup_screen(self):
    for widget in self.winfo_children():
      widget.pack_forget()
    # get all users
    lst_all_cur_users = self.get_current_users(DCM.root_dir)

    self.frm_signup_screen = customtkinter.CTkFrame(master=self, fg_color = DCM.bg_colour)
    self.frm_signup_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_backtologin_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_backtologin_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=15)

    # center screen frame
    customtkinter.CTkFrame(master=self.frm_signup_screen, width=357, height=601, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Sign Up label title
    customtkinter.CTkLabel(master=self.frm_signup_screen, text="Sign Up", width=143, height=63, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title, bg_color = DCM.gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)

    # email text 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text="Email", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=201)
    
    # email text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Enter Email", width=295, height=39, fg_color=DCM.white_1, 
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_username.place(relx = 0.5, rely=0.35, anchor=CENTER)

    # username text 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text="Username", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=278)
    
    # username text box
    self.txtbx_username = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Enter Username", width=295, height=39, fg_color=DCM.white_1, 
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_username.place(relx = 0.5, rely=0.46, anchor=CENTER)

    # password text 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text="Password", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=355)
    
    # password text box
    self.txtbx_password = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_password.place(relx = 0.5, rely=0.57, anchor=CENTER)

    # confirm password text 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text="Confirm Password", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=355, y=432)
    
    # confirm password text box
    self.txtbx_password = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Confirm Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_password.place(relx = 0.5, rely=0.68, anchor=CENTER)

    # x/10 users label 
    active_users = len(lst_all_cur_users) #temporary 
    maximum_users = 10 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text= str(active_users) + "/" + str(maximum_users) + " Users", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)
  
    # sign up button
    customtkinter.CTkButton(master=self.frm_signup_screen, width = 191, height=43, text="Sign Up", font=font_buttons,
                            state="normal",corner_radius=40, fg_color=DCM.blue_1, bg_color = DCM.gray_1).place(relx = 0.5, rely = 0.80, anchor = CENTER)
    
    # Back to login button
    backtologin_button = customtkinter.CTkButton(master=self.frm_signup_screen, width=20, height=25, text="< Back to Login", font=font_backtologin_labels,
                                        state="normal", fg_color=DCM.bg_colour, text_color=DCM.gray_2, hover_color=DCM.bg_colour, bg_color=DCM.bg_colour, command=self.back_to_login)
    backtologin_button.place(relx=0.1, rely=0.95, anchor=CENTER)
    backtologin_button.bind("<Enter>", lambda e: backtologin_button.configure(font=font_backtologin_labels_underlined))
    backtologin_button.bind("<Leave>", lambda e: backtologin_button.configure(font=font_backtologin_labels))

  ''' Other Methods '''

  #def sign_up_check(self, username, password):
  #  print(username)
  #  print(password)

  # opens a top level window if username or password is incorrect
  def open_credential_prompt(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = credential_prompt()  # create window if its None or destroyed
            self.toplevel_window.focus()
            self.toplevel_window.grab_set() # focus window and cant close it
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.grab_set() # focus window and cant close it

 # opens a top level window if user wants to access admin privileges
  def open_admin_login(self):
    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
      self.toplevel_window =  admin_login()  # create window if its None or destroyed
      self.toplevel_window.focus()
      self.toplevel_window.grab_set() # focus window and cant close it
    else:
      self.toplevel_window.focus()  # if window exists focus it
      self.toplevel_window.grab_set() # focus window and cant close it

  # function to read all of the json file user data
  def get_current_users(self, root_dir):
    all_user_data = [entry for entry in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, entry))]
    all_emails = []
    for user_file in all_user_data:
      with open(f"{DCM.root_dir}/{user_file}", 'r') as file:
        dict_user = json.load(file)
        all_emails.append(dict_user["_email"])
        
    return [all_user_data, all_emails]
  
  # attempt a login with the username and password
  def attempt_login(self, username, password, all_user_data):
    if f"{username}.json" in all_user_data[0]: # check for username
      with open(f"{DCM.root_dir}/{username}.json", 'r') as file:
        dict_user = json.load(file)
        
      if password == dict_user["_password"]:
        current_user = user.load_from_json(dict_user)
        self.create_main_interface(current_user)
      else:
        dict_user.clear()
        self.open_credential_prompt()

    elif username in all_user_data[1]: # check for email is in system
      associated_user = all_user_data[0][all_user_data[1].index(username)] # associates an email with a username
      with open(f"{DCM.root_dir}/{associated_user}", 'r') as file: # opens that users file
        dict_user = json.load(file)
      
      if password == dict_user["_password"]: # if passwords match then login
        current_user = user.load_from_json(dict_user)
        self.create_main_interface(current_user)
      else: # if it doesnt match then clear and give a notificaiton
        dict_user.clear()
        self.open_credential_prompt()

    else:
        self.open_credential_prompt()
  
''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()