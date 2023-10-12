''' Import Libraries '''
from tkinter import *
import customtkinter
from tkinter import font
import json
import os

''' Import External file variables and classes '''
from program_files.user_class import user

from program_files.app_widgets import successful_register_prompt
from program_files.app_widgets import admin_login
from program_files.app_widgets import delete_account
from program_files.app_widgets import scroll_parameters_frame

from program_files.app_colors import *
from program_files.mode_variables import *

''' Main App Class '''
# Main app classs
class DCM(customtkinter.CTk):
  ''' Constructor Method '''
  def __init__(self):
    super().__init__()
    # variables too be monitored devlared here
    self._perms = StringVar(value="Client")
    self._can_edit = BooleanVar(value=False)
    self._mode_choice = StringVar(value="None")
    self._updated_parameter_values = None
    self._connected_status = StringVar(value="Not Connected")
    self._battery_level = StringVar(value="N/A")

    self._all_battery_statuses = ['BOL', 'ERN', 'ERT', 'ERP'] # battery statuses for eventual implementation

    # monitor variables
    self._perms.trace_add("write", self._callback)
    self._can_edit.trace_add("write", self._callupdate)
    self._mode_choice.trace_add("write", self._callupdate)

    self._current_user = None # current user that is logged in is initially set to none

    self._admin_password = "coffee" # admin password
    self._root_dir = 'user_data'

    # intiialize window and begin the call for the first screen
    self.title("G29 - MECHTRON 3K04 - DCM")
    self.geometry("1000x700")
    self.resizable(height=False, width=False)
    self._create_login_screen()
    self._toplevel_window = None

  
  ''' Methods for page navigation '''
  # login screen
  def _create_login_screen(self):
    # get all users

    lst_all_cur_users = self._get_current_users(self._root_dir)

    self._frm_login_screen = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_login_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_signup = customtkinter.CTkFont(family="Lexend", weight="bold",size=12)
    font_signup_underline = customtkinter.CTkFont(family="Lexend", weight="bold", underline = 1, size=12)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)

    # center screen frame
    customtkinter.CTkFrame(master=self._frm_login_screen, width=357, height=601, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Login label title
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Login", width=143, height=63, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)
    
    # username text 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Username or Email", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=235)
    
    # username text box
    self._txtbx_username = customtkinter.CTkEntry(master=self._frm_login_screen, placeholder_text="Enter Username or Email", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_username.place(relx = 0.5, rely=0.4, anchor=CENTER)
    
    # password text 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=340)
    
    # password text box
    self._txtbx_password = customtkinter.CTkEntry(master=self._frm_login_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_password.place(relx = 0.5, rely=0.55, anchor=CENTER)


    # sign in button
    customtkinter.CTkButton(master=self._frm_login_screen, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=blue_1, bg_color = gray_1, command = lambda:self._attempt_login(self._txtbx_username.get(), self._txtbx_password.get(), lst_all_cur_users, self._root_dir)).place(relx = 0.5, rely = 0.7, anchor = CENTER)

    # watch for keystrokes
    self.bind("<Return>", lambda e:self._attempt_login(self._txtbx_username.get(), self._txtbx_password.get(), lst_all_cur_users, self._root_dir))

    # "Don't Have an Account?" label 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Don't Have an Account?", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_sub_labels, bg_color = gray_1).place(relx=0.475, rely=0.76, anchor=CENTER)


    # forgot password button
    self._forgot_button = customtkinter.CTkButton(master=self._frm_login_screen, width = 20, height=25, text="Forgot Password?", font=font_sub_labels, 
                            state="normal", fg_color=gray_1, text_color=gray_2, hover_color = gray_1, bg_color = gray_1)
    self._forgot_button.place(relx=0.592, rely=0.6, anchor=CENTER)
    self._forgot_button.bind("<Enter>", lambda e: self._forgot_button.configure(font=font_sub_labels_underlined))
    self._forgot_button.bind("<Leave>", lambda e: self._forgot_button.configure(font=font_sub_labels))

    # x/10 users label 
    active_users = len(lst_all_cur_users[0])
    maximum_users = 10 
    customtkinter.CTkLabel(master=self._frm_login_screen, text=f"{active_users}/{maximum_users} Users", width=100, height=25, fg_color=gray_1, text_color=gray_2 if active_users < maximum_users else red_1, font=font_sub_labels, bg_color = gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)

    # sign up button
    self._signup_button = customtkinter.CTkButton(master=self._frm_login_screen, width=20, height=25, text="Sign Up", font=font_signup,
                                        state="normal" if active_users < maximum_users else "disabled", fg_color=gray_1, text_color=blue_1, text_color_disabled=red_1, hover_color=gray_1, 
                                        bg_color=gray_1, command=self._create_signup_screen)
    self._signup_button.place(relx=0.575, rely=0.76, anchor=CENTER)
    self._signup_button.bind("<Enter>", lambda e: self._signup_button.configure(font=font_signup_underline))
    self._signup_button.bind("<Leave>", lambda e: self._signup_button.configure(font=font_signup))

  # main interface
  def _create_main_interface(self):
    for widget in self.winfo_children():
      widget.pack_forget()
    
    #fonts
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_username = customtkinter.CTkFont(family="Lexend", weight="bold",size=35)
    font_sections = customtkinter.CTkFont(family="Lexend", weight="bold",size=24)
    font_curmode = customtkinter.CTkFont(family="Lexend", size=20)
    font_connect = customtkinter.CTkFont(family="Lexend", size=15)

    #frame
    self._frm_main_interface = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_main_interface.pack(fill='both', expand=True)
   
    #admin button
    self._btn_admin = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Admin", state="normal", font=font_buttons, fg_color=blue_1, command=self._open_admin_login)
    self._btn_admin.place(x = 22, y = 306)

    #run button 
    self._btn_run = customtkinter.CTkButton(master=self._frm_main_interface, width = 117, height=43, text="Run", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=green_2, border_width=2, border_color=green_1, command=lambda:self._start_button_cmd(self._mode_choice.get()))
    self._btn_run.place(x = 22, y = 368)

    #stop button 
    self._btn_stop = customtkinter.CTkButton(master=self._frm_main_interface, width = 117, height=43, text="Stop", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=red_2, border_width=2, border_color=red_1, command=self._stop_button_cmd)
    self._btn_stop.place(x = 159, y = 368)

    #sign out button 
    customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Sign Out", state="normal", font=font_buttons, fg_color=blue_1, command=self._sign_out).place(x = 22, y = 546)
    
    #delete account button 
    self._btn_delete = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=33, text="Delete Account", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=red_2, border_width=2, border_color=red_1,  command=self._open_delete_account)
    self._btn_delete.place(x = 22, y = 603)
  
    #text for permissions
    self._perm_label = customtkinter.CTkLabel(master=self._frm_main_interface, text=f"Permission: {self._perms.get()}", width=143, height=34, fg_color=bg_colour, text_color=gray_3, font=font_buttons)
    self._perm_label.place(x=22, y=651)
    #text for username
    customtkinter.CTkLabel(master=self._frm_main_interface, text=f'{self._current_user.get_username()}', width=199, height=40, fg_color=bg_colour, text_color=white_1, font=font_username, justify="left", anchor="w").place(x=22, y=49)
    #text for mode
    customtkinter.CTkLabel(master=self._frm_main_interface, text="Mode", width=67, height=30, fg_color=bg_colour, text_color=gray_3, font=font_sections).place(x=22, y=104)
    #text for current mode
    self._current_mode_lbl = customtkinter.CTkLabel(master=self._frm_main_interface, text=f"Current Mode: {self._current_user.get_current_mode()}", width=200, height=15, fg_color=bg_colour, text_color=gray_3, font=font_curmode)
    self._current_mode_lbl.place(x=22, y=188)

    #text for parameters
    customtkinter.CTkLabel(master=self._frm_main_interface, text="Parameters", width=142, height=30, fg_color=bg_colour, text_color=gray_3, font=font_sections).place(x=300, y=49)
  
    #text for connected
    customtkinter.CTkLabel(master=self._frm_main_interface, text="⦿ Connected", width=154, height=34, fg_color=bg_colour, text_color=gray_3, font=font_connect, justify="left", anchor="w").place(x=22, y=9)

    ''' Code for the scrollable frame and the items in it for each parameter '''
    self._frm_scroll_parameters = scroll_parameters_frame(master=self._frm_main_interface, can_edit=self._can_edit.get(), width=665, height=585, fg_color=gray_1, send_data_func=self._get_parameter_data)
    self._frm_scroll_parameters.place(x=303,y=92)

    # dropdown menu for modes
    def load_parameters_from_mode(choice):
      self._mode_choice.set(choice)
    
    # function when the edit/save button is pressed
    def press_edit():
      new_can_edit = False if self._can_edit.get() else True
      if new_can_edit: # code if edit button is rpessed
        self._btn_edit.configure(text="Save")
      else: # code if save button is pressed
        self._btn_edit.configure(text="Edit")
        # save the parameters
        if self._mode_choice.get() != "None" and self._updated_parameter_values != None:
          dict_mode_parameters_for_user = self._current_user.get_all_mode_data()
    
          parameters_for_mode = dict_mode_parameters_for_user[self._mode_choice.get()]
          for index, parameter in enumerate(parameters_for_mode):
            parameters_for_mode[parameter] = self._updated_parameter_values[index]
          dict_mode_parameters_for_user[self._mode_choice.get()] = parameters_for_mode

          self._current_user.set_all_mode_data(dict_mode_parameters_for_user)
          self._current_user.save_to_json(self._root_dir)

      # update the current perms
      self._can_edit.set(new_can_edit)

    # edit button
    self._btn_edit = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Edit", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=orange_2, border_width=2, 
                                            border_color=orange_1, command=press_edit)
    self._btn_edit.place(x = 22, y = 430)

    str_default_text_mode = StringVar(value="Select a Mode")
    available_modes = [mode for mode in dict_modes]
    self._combobox_select_mode = customtkinter.CTkOptionMenu(master=self._frm_main_interface, values=available_modes, width=252, height=43, font=font_buttons, anchor="center",dynamic_resizing=True, command=load_parameters_from_mode,
                                                            dropdown_font=font_connect, fg_color=blue_1, dropdown_fg_color=blue_2, dropdown_hover_color=blue_3, corner_radius=15, bg_color=bg_colour, variable=str_default_text_mode)
    self._combobox_select_mode.place(x=23,y=147)

  # navigate back to log in screen
  def _back_to_login(self):
    for widget in self.winfo_children():
      widget.destroy()
    self._create_login_screen()
  
  # register an account page
  def _create_signup_screen(self):
    # get all users
    lst_all_cur_users = self._get_current_users(self._root_dir)
    for widget in self.winfo_children():
      widget.destroy()

    self._frm_signup_screen = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_signup_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_backtologin_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_backtologin_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=15)

    # center screen frame
    customtkinter.CTkFrame(master=self._frm_signup_screen, width=357, height=601, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Sign Up label title
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Sign Up", width=143, height=63, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)

    # email text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Email", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=201)
    
    # email text box
    self._txtbx_email = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Email", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_email.place(relx = 0.5, rely=0.35, anchor=CENTER)

    # username text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Username", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=278)
    
    # username text box
    self._txtbx_username = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Username", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_username.place(relx = 0.5, rely=0.46, anchor=CENTER)

    # password text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=355)
    
    # password text box
    self._txtbx_password = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_password.place(relx = 0.5, rely=0.57, anchor=CENTER)

    # confirm password text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Confirm Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=432)
    
    # confirm password text box
    self._txtbx_confirm_password = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Confirm Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_confirm_password.place(relx = 0.5, rely=0.68, anchor=CENTER)

    # sign up button
    sign_up_page_button = customtkinter.CTkButton(master=self._frm_signup_screen, width = 191, height=43, text="Sign Up", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=blue_1, bg_color = gray_1, command=lambda: self._sign_up_check(self._txtbx_username.get(), self._txtbx_email.get(), self._txtbx_password.get(), self._txtbx_confirm_password.get()))
    sign_up_page_button.place(relx = 0.5, rely = 0.80, anchor = CENTER)

    # x/10 users label 
    active_users = len(lst_all_cur_users[0]) #temporary 
    maximum_users = 10 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text= str(active_users) + "/" + str(maximum_users) + " Users", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_sub_labels, bg_color = gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)

    # Back to login button
    backtologin_button = customtkinter.CTkButton(master=self._frm_signup_screen, width=20, height=25, text="< Back to Login", font=font_backtologin_labels,
                                        state="normal", fg_color=bg_colour, text_color=gray_2, hover_color=bg_colour, bg_color=bg_colour, command=self._back_to_login)
    backtologin_button.place(relx=0.1, rely=0.95, anchor=CENTER)
    backtologin_button.bind("<Enter>", lambda e: backtologin_button.configure(font=font_backtologin_labels_underlined))
    backtologin_button.bind("<Leave>", lambda e: backtologin_button.configure(font=font_backtologin_labels))

  # sign out function
  def _sign_out(self):
    self._mode_choice.set("None")
    self._can_edit.set(False)
    self._perms.set("Client")
    self._current_user = None
    self._back_to_login()


  ''' Other Methods '''

  #Check if register user is valid
  def _sign_up_check(self, username, email, password, confirm_password):
    list_users = self._get_current_users(self._root_dir)
    c = len(list_users[0])
    remove_term = ".json"
    stat = 1

    for i in range(c):
      strip_username = list_users[0][i].replace(remove_term, '')
      if strip_username == username:
        stat = 0
        self._open_username_taken_prompt()
        break
      elif list_users[1][i] == email:
        stat = 0
        self._open_email_taken_prompt()
        break
      else:
        continue
    if password != confirm_password or password == '' or confirm_password == '':
      stat = 0 
      self._open_password_confirm_bad_prompt()

    if stat == 1:
      new_user = user(username = username, password = password, email = email)
      new_user.save_to_json(self._root_dir)
      self._create_signup_screen()
      self._back_to_login()
      self._open_successful_register_prompt()

  # opens a prompt if username or password is incorrect
  def _open_credential_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_login_screen, text = "Username and/or Password is incorrect", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=385, y=445)

  # opens a prompt for admin login if admin password is incorrect
  def _open_admin_credential_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_admin_login_screen, text = "Admin Password is incorrect", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=115, y=435)

    # opens a prompt for delete account if admin password is incorrect
  def _open_delete_admin_credential_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_delete_account_screen, text = "Admin Password is incorrect", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=115, y=465)
    print("okok")

  # opens a top level window if register is successful
  def _open_successful_register_prompt(self):
    if self._toplevel_window is None or not self._toplevel_window.winfo_exists():
        self._toplevel_window = successful_register_prompt()  # create window if its None or destroyed
        self._toplevel_window.focus()
        self._toplevel_window.grab_set() # focus window and cant close it
    else:
        self._toplevel_window.focus()  # if window exists focus it
        self._toplevel_window.grab_set() # focus window and cant close it
  
  # opens a prompt if username is taken
  def _open_username_taken_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Username is already taken", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=490, y=281)
  
  # opens a prompt if email is incorrect
  def _open_email_taken_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Email is already taken", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=515, y=204)

  # opens a prompt if password and confirm password do not match
  def _open_password_confirm_bad_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Confirm Password Invalid", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=495, y=435)

 # opens a top level window if user wants to access admin privileges
  def _open_admin_login(self):
    self._frm_admin_login_screen = self._toplevel_window
    if self._frm_admin_login_screen is None or not self._frm_admin_login_screen.winfo_exists():
      self._frm_admin_login_screen =  admin_login(self._submit_admin_password)  # create window if its None or destroyed
      self._frm_admin_login_screen.focus()
      self._frm_admin_login_screen.grab_set() # focus window and cant close it
    else:
      self._frm_admin_login_screen.focus()  # if window exists focus it
      self._frm_admin_login_screen.grab_set() # focus window and cant close it

# opens a top level window if admin wants to delete a user account
  def _open_delete_account(self):
    self._frm_delete_account_screen = self._toplevel_window
    if self._frm_delete_account_screen is None or not self._frm_delete_account_screen.winfo_exists():
      self._frm_delete_account_screen =  delete_account(self.delete_account, self._admin_password)  # create window if its None or destroyed
      self._frm_delete_account_screen.focus()
      self._frm_delete_account_screen.grab_set() # focus window and cant close it
    else:
      self._frm_delete_account_screen.focus()  # if window exists focus it
      self._frm_delete_account_screen.grab_set() # focus window and cant close it

  # function to read all of the json file user data
  def _get_current_users(self, root_dir):
    all_user_data = [entry for entry in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, entry))]
    all_emails = []
    for user_file in all_user_data:
      with open(f"{root_dir}/{user_file}", 'r') as file:
        dict_user = json.load(file)
        all_emails.append(dict_user["_email"])
        
    return [all_user_data, all_emails]
  
  # attempt a login with the username and password
  def _attempt_login(self, username, password, all_user_data, root_dir):
    if f"{username}.json" in all_user_data[0]: # check for username
      with open(f"{root_dir}/{username}.json", 'r') as file:
        dict_user = json.load(file)
        
      if password == dict_user["_password"]:
        current_user = user.load_from_json(dict_user)
        self._current_user = current_user
        self._create_main_interface()
      else:
        dict_user.clear()
        self._open_credential_prompt()

    elif username in all_user_data[1]: # check for email is in system
      associated_user = all_user_data[0][all_user_data[1].index(username)] # associates an email with a username
      with open(f"{root_dir}/{associated_user}", 'r') as file: # opens that users file
        dict_user = json.load(file)
      
      if password == dict_user["_password"]: # if passwords match then login
        current_user = user.load_from_json(dict_user)
        self._current_user = current_user
        self._create_main_interface()
      else: # if it doesnt match then clear and give a notificaiton
        dict_user.clear()
        self._open_credential_prompt()

    else:
        self._open_credential_prompt()
  
  # submit the admin password from the popup window
  def _submit_admin_password(self, entered_admin_password):
    if entered_admin_password == self._admin_password:
      self._frm_admin_login_screen.destroy()
      self._perms.set("Admin")
    else:
      self._open_admin_credential_prompt()
  
  # delete the account
  def delete_account(self):
    self._current_user.delete_account(self._root_dir)
    self._current_user = None
    self._frm_delete_account_screen.destroy()
    self._back_to_login()

  # toggles the button between the normal and disabled state
  def _toggle_button(self, btn):
    current_state = btn.cget('state')
    new_state = "normal" if current_state == "disabled" else "disabled"
    if new_state == "disabled":
      btn.configure(state=new_state, fg_color=gray_1)
    elif new_state == "normal":
      btn.configure(state=new_state, fg_color=btn.cget("border_color"))
    
  def _disable_button(self, btn):
    btn.configure(state="disabled", fg_color=gray_1)
  
  def _enable_button(self, btn):
    btn.configure(state="normal", fg_color=btn.cget("border_color"))

  # function to retrieve data from the scrollable frame class with the sliders to bring it into the main app class
  def _get_parameter_data(self, values):
    self._updated_parameter_values = values
  
  # function to monitor changes to the current perms
  def _callback(self, *args):
    if self._perms.get() == "Admin": # going from client --> admin
      self._perm_label.configure(text=f"Permission: {self._perms.get()}")
      self._enable_button(self._btn_run)
      self._enable_button(self._btn_stop)
      self._enable_button(self._btn_delete)
      self._enable_button(self._btn_edit)
      self._btn_admin.configure(text="Sign Out Admin", command=lambda: self._perms.set("Client"))
    else: # going from admin --> client
      self._perm_label.configure(text=f"Permission: {self._perms.get()}")
      self._disable_button(self._btn_run)
      self._disable_button(self._btn_stop)
      self._disable_button(self._btn_delete)
      self._disable_button(self._btn_edit)
      self._can_edit.set(False)
      self._btn_edit.configure(text="Edit")
      self._btn_admin.configure(text="Admin", command=self._open_admin_login)

  # update funciton whenever the edit button is pressed or a new choice has been made from drop down menu
  def _callupdate(self, *args):
    if self._mode_choice.get() != 'None':
      self._frm_scroll_parameters.destroy() # destroy the current window so it prevents overlap
      dict_mode_parameters_for_user = self._current_user.get_all_mode_data()
      self._frm_scroll_parameters = scroll_parameters_frame(master=self._frm_main_interface, can_edit=self._can_edit.get(), width=665, height=585, fg_color=gray_1, current_mode=self._mode_choice.get(), current_mode_data=dict_mode_parameters_for_user[self._mode_choice.get()], send_data_func=self._get_parameter_data)
      self._frm_scroll_parameters.place(x=303,y=92)

  # command when the stop button is pressed
  def _stop_button_cmd(self):
    self._current_user.set_current_mode("Off")
    self._current_mode_lbl.configure(text=f'Current Mode: {self._current_user.get_current_mode()}')
    self._current_user.save_to_json(self._root_dir)

  # command when the start button is pressed
  def _start_button_cmd(self, selected_mode):
    self._current_user.set_current_mode(selected_mode)
    self._current_mode_lbl.configure(text=f'Current Mode: {self._current_user.get_current_mode()}')
    self._current_user.save_to_json(self._root_dir)
    self._send_parameters_to_simulink(selected_mode)
  
  # command to send the current user parameters to simulink
  def _send_parameters_to_simulink(self, selected_mode):
    pass

''' Main '''
if __name__ == "__main__":
  dcm = DCM()
  dcm.mainloop()