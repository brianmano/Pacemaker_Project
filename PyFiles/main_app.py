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

# class for letting the user know when they successfully register an account
class successful_register_prompt(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.geometry("400x200")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=15)
    self.label = customtkinter.CTkLabel(self, text="Successfully Registered!",font=font)
    self.label.pack(padx=20, pady=20)

#class for admin login
class admin_login(customtkinter.CTkToplevel):
  def __init__(self, submit_admin_password):
    super().__init__()
    self.geometry("400x600")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend Bold", size=40)
    self.label = customtkinter.CTkLabel(self, text="Admin Login",font=font)
    self.label.pack(padx=20, pady=20)
    self.get_admin_password = submit_admin_password
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
    
    txtbx_password = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    txtbx_password.place(x=50, y=362)
    # sign in button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=DCM.blue_1, bg_color = DCM.gray_1, command=lambda:self.send_password(txtbx_password.get())).place(x = 100, y=459)
    
    self.bind("<Return>", lambda e:self.send_password(txtbx_password.get()))
  
  def send_password(self, entered_password):
    self.get_admin_password(entered_password)

# class for deleteing account
class delete_account(customtkinter.CTkToplevel):
  def __init__(self, submit_delete_account_confirm):
    super().__init__()
    self.geometry("400x600")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend Bold", size=40)
    self.label = customtkinter.CTkLabel(self, text="Delete Account",font=font)
    self.label.pack(padx=20, pady=20)
    self.submit_delete_account_confirm = submit_delete_account_confirm
    #fonts
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=40)
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    # center screen frame
    customtkinter.CTkFrame(master=self, width=357, height=561, fg_color=DCM.gray_1, corner_radius=15, border_width=3, 
                           border_color=DCM.blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Delete Account label title
    customtkinter.CTkLabel(master=self, text="Delete Account", width=257, height=50, fg_color=DCM.gray_1, text_color=DCM.white_1, font=font_title, bg_color = DCM.gray_1).place(x=45, y=54)
    # password text 
    customtkinter.CTkLabel(master=self, text="Admin Password", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=50, y=270)
    
    txtbx_password = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    txtbx_password.place(x=50, y=291)
    # delete button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="DELETE", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=DCM.red_1, hover_color=DCM.red_2, bg_color = DCM.gray_1, command=lambda:self.send_comfirmation(txtbx_password.get())).place(x = 100, y=382)
    # cancel button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="CANCEL", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=DCM.blue_1, bg_color = DCM.gray_1, command=lambda: self.destroy()).place(x = 100, y=453)
    
    self.bind("<Return>", lambda e:self.send_comfirmation(txtbx_password.get()))
  
  def send_comfirmation(self, entered_password):
    if entered_password == DCM.admin_password:
      self.submit_delete_account_confirm()

# class for a scrollable frame in main interface
class scroll_parameters_frame(customtkinter.CTkScrollableFrame):
  def __init__(self, master, current_mode_data = None, current_mode = None, can_edit = None, send_data_func = None, **kwargs):
    super().__init__(master, **kwargs)

    # font
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=18)
    font2 = customtkinter.CTkFont(family="Lexend SemiBold", size=35)
    self.current_mode_data = current_mode_data
    self.send_data_func = send_data_func

    can_edit = can_edit

    if can_edit:
      state = "normal"
      color = DCM.blue_1
    else:
      state = "disabled"
      color = DCM.gray_2

    # checks if a mode is actually sleected, will be none when the main interface is first launched
    if current_mode != None:
      self.parameter_value_list = [0] * len(current_mode_data)
      self.parameter_sliders = [customtkinter.CTkSlider(master=self, progress_color=color, state=state) for i in range(len(current_mode_data))] # make a list of obj for sliders based on how many parameters
      self.parameter_values_label = [customtkinter.CTkLabel(master=self, font=font, width=100, height=60, anchor="e") for i in range(len(current_mode_data))] # make a list of obj for labels based on how many parameters

      # slider even to change the number displayed on the label
      def slider_event(value, index, parameter):
        self.parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][int(value)]} {dict_param_and_range[parameter][1]}' if not isinstance(dict_param_and_range[parameter][0][int(value)],str) else f'{dict_param_and_range[parameter][0][int(value)]}')
        self.parameter_value_list[index] = dict_param_and_range[parameter][0][int(value)]
        self.update_changes() # updates the current changes list

      # iterate through the all the parameters needed and makes the corresponding widgets
      for index, parameter in enumerate(current_mode_data):
        customtkinter.CTkLabel(master=self, text=parameter, font=font, width=220, height=60, anchor="w").grid(row=index, column=0, padx=30, pady=20)

        self.parameter_sliders[index].configure(from_=0, to=len(dict_param_and_range[parameter][0])-1, number_of_steps=len(dict_param_and_range[parameter][0]),
                                      command=lambda value=self.parameter_sliders[index].get(), index=index, parameter=parameter: slider_event(value,index,parameter))
        self.parameter_sliders[index].grid(row=index, column=1, columnspan=3, padx=0, pady=20)
        self.parameter_sliders[index].set(dict_param_and_range[parameter][0].index(current_mode_data[parameter]))
    
        self.parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][dict_param_and_range[parameter][0].index(current_mode_data[parameter])]} {dict_param_and_range[parameter][1]}' if not isinstance(current_mode_data[parameter],str) else f'{current_mode_data[parameter]}')
        self.parameter_values_label[index].grid(row=index, column=5, padx=30, pady=20)

        # updating the value list containing all the most recent data
        self.parameter_value_list[index] = dict_param_and_range[parameter][0][dict_param_and_range[parameter][0].index(current_mode_data[parameter])]
    
    else:
      customtkinter.CTkLabel(master=self, font=font2, text="Select a Mode", text_color=DCM.gray_2, anchor="center").grid(row=0,column=0,padx=210, pady=240)

  # sends the list of data to the main class whenever a slider is cahnged
  def update_changes(self):
    self.send_data_func(self.parameter_value_list)
  
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

  orange_1 = "#D18034"
  orange_2 = "#d18f52"

  # root file dir
  root_dir = 'user_data'

  admin_password = "coffee"

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

    self.perms = StringVar(value="Client")
    self.can_edit = BooleanVar(value=False)
    self.mode_choice = StringVar(value="None")
    self.updated_parameter_values = None

    # monitor variables
    self.perms.trace_add("write", self.callback)
    self.can_edit.trace_add("write", self.callupdate)
    self.mode_choice.trace_add("write", self.callupdate)

    self.current_user = None
  
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

    # watch for keystrokes
    self.bind("<Return>", lambda e:self.attempt_login(self.txtbx_username.get(), self.txtbx_password.get(), lst_all_cur_users))

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
  def create_main_interface(self):
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
    self.btn_admin = customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=43, text="Admin", state="normal", font=font_buttons, fg_color=DCM.blue_1, command=self.open_admin_login)
    self.btn_admin.place(x = 22, y = 306)

    #run button 
    self.btn_run = customtkinter.CTkButton(master=self.frm_main_interface, width = 117, height=43, text="Run", state="disabled", font=font_buttons, fg_color=DCM.gray_1, hover_color=DCM.green_2, border_width=2, border_color=DCM.green_1)
    self.btn_run.place(x = 22, y = 368)

    #stop button 
    self.btn_stop = customtkinter.CTkButton(master=self.frm_main_interface, width = 117, height=43, text="Stop", state="disabled", font=font_buttons, fg_color=DCM.gray_1, hover_color=DCM.red_2, border_width=2, border_color=DCM.red_1)
    self.btn_stop.place(x = 159, y = 368)

    #sign out button 
    customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=43, text="Sign Out", state="normal", font=font_buttons, fg_color=DCM.blue_1, command=self.sign_out).place(x = 22, y = 546)
    
    #delete account button 
    self.btn_delete = customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=33, text="Delete Account", state="disabled", font=font_buttons, fg_color=DCM.gray_1, hover_color=DCM.red_2, border_width=2, border_color=DCM.red_1,  command=self.open_delete_account)
    self.btn_delete.place(x = 22, y = 603)
  
    #text for permissions
    self.perm_label = customtkinter.CTkLabel(master=self.frm_main_interface, text=f"Permission: {self.perms.get()}", width=143, height=34, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_buttons)
    self.perm_label.place(x=22, y=651)
    #text for username
    customtkinter.CTkLabel(master=self.frm_main_interface, text=f'{self.current_user.get_username()}', width=199, height=40, fg_color=DCM.bg_colour, text_color=DCM.white_1, font=font_username, justify="left", anchor="w").place(x=22, y=49)
    #text for mode
    customtkinter.CTkLabel(master=self.frm_main_interface, text="Mode", width=67, height=30, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_sections).place(x=22, y=104)
    #text for current mode
    customtkinter.CTkLabel(master=self.frm_main_interface, text=f"Current Mode: {self.current_user.get_current_mode()}", width=200, height=15, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_curmode).place(x=22, y=188)
    #text for parameters
    customtkinter.CTkLabel(master=self.frm_main_interface, text="Parameters", width=142, height=30, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_sections).place(x=300, y=49)
  
    #text for connected
    customtkinter.CTkLabel(master=self.frm_main_interface, text="⦿ Connected", width=154, height=34, fg_color=DCM.bg_colour, text_color=DCM.gray_3, font=font_connect, justify="left", anchor="w").place(x=22, y=9)

    ''' Code for the scrollable frame and the items in it for each parameter '''
    self.frm_scroll_parameters = scroll_parameters_frame(master=self.frm_main_interface, can_edit=self.can_edit.get(), width=665, height=585, fg_color=DCM.gray_1, send_data_func=self.get_parameter_data)
    self.frm_scroll_parameters.place(x=303,y=92)

    # dropdown menu for modes
    def load_parameters_from_mode(choice):
      self.mode_choice.set(choice)
    
    # function when the edit/save button is pressed
    def press_edit():
      new_can_edit = False if self.can_edit.get() else True
      if new_can_edit: # code if edit button is rpessed
        self.btn_edit.configure(text="Save")
      else: # code if save button is pressed
        self.btn_edit.configure(text="Edit")
        # save the parameters
        if self.mode_choice.get() != "None" and self.updated_parameter_values != None:
          dict_mode_parameters_for_user = self.current_user.get_all_mode_data()
    
          parameters_for_mode = dict_mode_parameters_for_user[self.mode_choice.get()]
          for index, parameter in enumerate(parameters_for_mode):
            parameters_for_mode[parameter] = self.updated_parameter_values[index]
          dict_mode_parameters_for_user[self.mode_choice.get()] = parameters_for_mode

          self.current_user.set_all_mode_data(dict_mode_parameters_for_user)
          self.current_user.save_to_json(DCM.root_dir)

      # update the current perms
      self.can_edit.set(new_can_edit)

    # edit button
    self.btn_edit = customtkinter.CTkButton(master=self.frm_main_interface, width = 252, height=43, text="Edit", state="disabled", font=font_buttons, fg_color=DCM.gray_1, hover_color=DCM.orange_2, border_width=2, 
                                            border_color=DCM.orange_1, command=press_edit)
    self.btn_edit.place(x = 22, y = 430)

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
    # get all users
    lst_all_cur_users = self.get_current_users(DCM.root_dir)
    for widget in self.winfo_children():
      widget.pack_forget()

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
    self.txtbx_email = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Enter Email", width=295, height=39, fg_color=DCM.white_1, 
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_email.place(relx = 0.5, rely=0.35, anchor=CENTER)

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
    self.txtbx_confirm_password = customtkinter.CTkEntry(master=self.frm_signup_screen, placeholder_text="Confirm Password", width=295, height=39, fg_color=DCM.white_1, show="•",
                                                text_color=DCM.gray_1, placeholder_text_color=DCM.gray_2, font=font_text_box, corner_radius=5, bg_color=DCM.gray_1)
    self.txtbx_confirm_password.place(relx = 0.5, rely=0.68, anchor=CENTER)

    # sign up button
    sign_up_page_button = customtkinter.CTkButton(master=self.frm_signup_screen, width = 191, height=43, text="Sign Up", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=DCM.blue_1, bg_color = DCM.gray_1, command=lambda: self.sign_up_check(self.txtbx_username.get(), self.txtbx_email.get(), self.txtbx_password.get(), self.txtbx_confirm_password.get()))
    sign_up_page_button.place(relx = 0.5, rely = 0.80, anchor = CENTER)

    # x/10 users label 
    active_users = len(lst_all_cur_users[0]) #temporary 
    maximum_users = 10 
    customtkinter.CTkLabel(master=self.frm_signup_screen, text= str(active_users) + "/" + str(maximum_users) + " Users", width=100, height=25, fg_color=DCM.gray_1, text_color=DCM.gray_2, font=font_sub_labels, bg_color = DCM.gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)

    # Back to login button
    backtologin_button = customtkinter.CTkButton(master=self.frm_signup_screen, width=20, height=25, text="< Back to Login", font=font_backtologin_labels,
                                        state="normal", fg_color=DCM.bg_colour, text_color=DCM.gray_2, hover_color=DCM.bg_colour, bg_color=DCM.bg_colour, command=self.back_to_login)
    backtologin_button.place(relx=0.1, rely=0.95, anchor=CENTER)
    backtologin_button.bind("<Enter>", lambda e: backtologin_button.configure(font=font_backtologin_labels_underlined))
    backtologin_button.bind("<Leave>", lambda e: backtologin_button.configure(font=font_backtologin_labels))

  # sign out function
  def sign_out(self):
    self.mode_choice.set("None")
    self.can_edit.set(False)
    self.perms.set("Client")
    self.current_user = None
    self.back_to_login()


  ''' Other Methods '''

  #Check if register user is valid
  def sign_up_check(self, username, email, password, confirm_password):
    list_users = self.get_current_users(DCM.root_dir)
    c = len(list_users[0])
    remove_term = ".json"
    stat = 1

    for i in range(c):
      strip_username = list_users[0][i].replace(remove_term, '')
      if strip_username == username:
        stat = 0
        self.open_username_taken_prompt()
        break
      elif list_users[1][i] == email:
        stat = 0
        self.open_email_taken_prompt()
        break
      else:
        continue
    if password != confirm_password or password == '' or confirm_password == '':
      stat = 0 
      self.open_password_confirm_bad_prompt()

    if stat == 1:
      new_user = user(username = username, password = password, email = email)
      new_user.save_to_json(DCM.root_dir)
      self.create_signup_screen()
      self.back_to_login()
      self.open_successful_register_prompt()

  # opens a top level window if username or password is incorrect
  def open_credential_prompt(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = credential_prompt()  # create window if its None or destroyed
            self.toplevel_window.focus()
            self.toplevel_window.grab_set() # focus window and cant close it
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.grab_set() # focus window and cant close it

  # opens a top level window if register is successful
  def open_successful_register_prompt(self):
      if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
          self.toplevel_window = successful_register_prompt()  # create window if its None or destroyed
          self.toplevel_window.focus()
          self.toplevel_window.grab_set() # focus window and cant close it
      else:
          self.toplevel_window.focus()  # if window exists focus it
          self.toplevel_window.grab_set() # focus window and cant close it
  
  # opens a top level window if username is taken
  def open_username_taken_prompt(self):
      font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
      customtkinter.CTkLabel(master=self.frm_signup_screen, text = "Username is already taken", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.red_1, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=490, y=281)
  
  # opens a top level window if email is incorrect
  def open_email_taken_prompt(self):
      font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
      customtkinter.CTkLabel(master=self.frm_signup_screen, text = "Email is already taken", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.red_1, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=515, y=204)

  # opens a top level window if password and confirm password do not match
  def open_password_confirm_bad_prompt(self):
      font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
      customtkinter.CTkLabel(master=self.frm_signup_screen, text = "Confirm Password Invalid", width=10, height=20, fg_color=DCM.gray_1, text_color=DCM.red_1, font=font_user_pass_labels, bg_color = DCM.gray_1).place(x=495, y=435)

 # opens a top level window if user wants to access admin privileges
  def open_admin_login(self):
    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
      self.toplevel_window =  admin_login(self.submit_admin_password)  # create window if its None or destroyed
      self.toplevel_window.focus()
      self.toplevel_window.grab_set() # focus window and cant close it
    else:
      self.toplevel_window.focus()  # if window exists focus it
      self.toplevel_window.grab_set() # focus window and cant close it

# opens a top level window if admin wants to delete a user account
  def open_delete_account(self):
    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
      self.toplevel_window =  delete_account(self.delete_account)  # create window if its None or destroyed
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
        self.current_user = current_user
        self.create_main_interface()
      else:
        dict_user.clear()
        self.open_credential_prompt()

    elif username in all_user_data[1]: # check for email is in system
      associated_user = all_user_data[0][all_user_data[1].index(username)] # associates an email with a username
      with open(f"{DCM.root_dir}/{associated_user}", 'r') as file: # opens that users file
        dict_user = json.load(file)
      
      if password == dict_user["_password"]: # if passwords match then login
        current_user = user.load_from_json(dict_user)
        self.current_user = current_user
        self.create_main_interface()
      else: # if it doesnt match then clear and give a notificaiton
        dict_user.clear()
        self.open_credential_prompt()

    else:
        self.open_credential_prompt()
  
  # submit the admin password from the popup window
  def submit_admin_password(self, entered_admin_password):
    if entered_admin_password == DCM.admin_password:
      self.toplevel_window.destroy()
      self.perms.set("Admin")
  
  # delete the account
  def delete_account(self):
    self.current_user.delete_account(DCM.root_dir)
    self.current_user = None
    self.toplevel_window.destroy()
    self.back_to_login()

  # toggles the button between the normal and disabled state
  def toggle_button(self, btn):
    current_state = btn.cget('state')
    new_state = "normal" if current_state == "disabled" else "disabled"
    if new_state == "disabled":
      btn.configure(state=new_state, fg_color=DCM.gray_1)
    elif new_state == "normal":
      btn.configure(state=new_state, fg_color=btn.cget("border_color"))

  # function to retrieve data from the scrollable frame class with the sliders to bring it into the main app class
  def get_parameter_data(self, values):
    self.updated_parameter_values = values
  
  # function to monitor changes to the current perms
  def callback(self, *args):
    if self.perms.get() == "Admin": # going from client --> admin
      self.perm_label.configure(text=f"Permission: {self.perms.get()}")
      self.toggle_button(self.btn_run)
      self.toggle_button(self.btn_stop)
      self.toggle_button(self.btn_delete)
      self.toggle_button(self.btn_edit)
      self.btn_admin.configure(text="Sign Out Admin", command=lambda: self.perms.set("Client"))
    else: # going from admin --> client
      self.perm_label.configure(text=f"Permission: {self.perms.get()}")
      self.toggle_button(self.btn_run)
      self.toggle_button(self.btn_stop)
      self.toggle_button(self.btn_delete)
      self.toggle_button(self.btn_edit)
      self.can_edit.set(False)
      self.btn_edit.configure(text="Edit")
      self.btn_admin.configure(text="Admin", command=self.open_admin_login)

  # update funciton whenever the edit button is pressed or a new choice has been made from drop down menu
  def callupdate(self, *args):
    if self.mode_choice.get() != 'None':
      dict_mode_parameters_for_user = self.current_user.get_all_mode_data()
      self.frm_scroll_parameters = scroll_parameters_frame(master=self.frm_main_interface, can_edit=self.can_edit.get(), width=665, height=585, fg_color=DCM.gray_1, current_mode=self.mode_choice.get(), current_mode_data=dict_mode_parameters_for_user[self.mode_choice.get()], send_data_func=self.get_parameter_data)
      self.frm_scroll_parameters.place(x=303,y=92)


''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()