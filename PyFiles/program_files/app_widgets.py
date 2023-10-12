''' Import Statements '''
from tkinter import *
import customtkinter
from tkinter import font

# colours for use
from .app_colors import *

# mode variables
from .mode_variables import *

# class for letting the user know when they successfully register an account
class successful_register_prompt(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.geometry("400x200")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=15)
    self._label = customtkinter.CTkLabel(self, text="Successfully Registered!",font=font)
    self._label.pack(padx=20, pady=20)

#class for admin login
class admin_login(customtkinter.CTkToplevel):
  def __init__(self, submit_admin_password):
    super().__init__()
    self.geometry("400x600")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend Bold", size=40)
    self._label = customtkinter.CTkLabel(self, text="Admin Login",font=font)
    self._label.pack(padx=20, pady=20)
    self._get_admin_password = submit_admin_password # assinging a private variable to a function that was passed in
    #fonts
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=40)
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    # center screen frame
    customtkinter.CTkFrame(master=self, width=357, height=561, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Admin Login label title
    customtkinter.CTkLabel(master=self, text="Admin Login", width=257, height=50, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(x=70, y=54)
    # password text 
    customtkinter.CTkLabel(master=self, text="Admin Password", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=50, y=337)
    
    txtbx_password = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    txtbx_password.place(x=50, y=362)
    # sign in button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=blue_1, bg_color = gray_1, command=lambda:self._send_password(txtbx_password.get())).place(x = 100, y=459)
    
    self.bind("<Return>", lambda e:self._send_password(txtbx_password.get()))
  
  def _send_password(self, entered_password):
    self._get_admin_password(entered_password)

# class for deleteing account
class delete_account(customtkinter.CTkToplevel):
  def __init__(self, submit_delete_account_confirm, admin_password):
    super().__init__()
    self.geometry("400x600")
    self.configure(fg_color="#1A1A1A")
    self.resizable(height=False, width=False)
    font = customtkinter.CTkFont(family="Lexend Bold", size=40)
    self._label = customtkinter.CTkLabel(self, text="Delete Account",font=font)
    self._label.pack(padx=20, pady=20)
    self._submit_delete_account_confirm = submit_delete_account_confirm
    self._admin_password = admin_password
    #fonts
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=40)
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    # center screen frame
    customtkinter.CTkFrame(master=self, width=357, height=561, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Delete Account label title
    customtkinter.CTkLabel(master=self, text="Delete Account", width=257, height=50, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(x=45, y=54)
    # password text 
    customtkinter.CTkLabel(master=self, text="Admin Password", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=50, y=270)
    
    txtbx_password = customtkinter.CTkEntry(master=self, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    txtbx_password.place(x=50, y=291)
    # delete button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="DELETE", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=red_1, hover_color=red_2, bg_color = gray_1, command=lambda:self._send_comfirmation(txtbx_password.get())).place(x = 100, y=382)
    # cancel button
    customtkinter.CTkButton(master=self, width = 191, height=43, text="CANCEL", font=font_buttons, 
                            state="normal",corner_radius=15, fg_color=blue_1, bg_color = gray_1, command=lambda: self.destroy()).place(x = 100, y=453)
    
    self.bind("<Return>", lambda e:self._send_comfirmation(txtbx_password.get()))
  
  def _send_comfirmation(self, entered_password):
    if entered_password == self._admin_password:
      self._submit_delete_account_confirm()

# class for a scrollable frame in main interface
class scroll_parameters_frame(customtkinter.CTkScrollableFrame):
  def __init__(self, master, current_mode_data = None, current_mode = None, can_edit = None, send_data_func = None, **kwargs):
    super().__init__(master, **kwargs)

    # font
    font = customtkinter.CTkFont(family="Lexend SemiBold", size=18)
    font2 = customtkinter.CTkFont(family="Lexend SemiBold", size=35)
    self._current_mode_data = current_mode_data
    self._send_data_func = send_data_func

    can_edit = can_edit

    if can_edit:
      state = "normal"
      color = blue_1
    else:
      state = "disabled"
      color = gray_2

    # checks if a mode is actually sleected, will be none when the main interface is first launched
    if current_mode != None:
      self._parameter_value_list = [0] * len(current_mode_data)
      self._parameter_sliders = [customtkinter.CTkSlider(master=self, progress_color=color, state=state) for i in range(len(current_mode_data))] # make a list of obj for sliders based on how many parameters
      self._parameter_values_label = [customtkinter.CTkLabel(master=self, font=font, width=100, height=60, anchor="e") for i in range(len(current_mode_data))] # make a list of obj for labels based on how many parameters

      # slider even to change the number displayed on the label
      def slider_event(value, index, parameter):
        self._parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][int(value)]} {dict_param_and_range[parameter][1]}' if not isinstance(dict_param_and_range[parameter][0][int(value)],str) else f'{dict_param_and_range[parameter][0][int(value)]}')
        self._parameter_value_list[index] = dict_param_and_range[parameter][0][int(value)]
        self._update_changes() # updates the current changes list

      # iterate through the all the parameters needed and makes the corresponding widgets
      for index, parameter in enumerate(current_mode_data):
        customtkinter.CTkLabel(master=self, text=parameter, font=font, width=220, height=60, anchor="w").grid(row=index, column=0, padx=30, pady=20)

        self._parameter_sliders[index].configure(from_=0, to=len(dict_param_and_range[parameter][0])-1, number_of_steps=len(dict_param_and_range[parameter][0]),
                                      command=lambda value=self._parameter_sliders[index].get(), index=index, parameter=parameter: slider_event(value,index,parameter))
        self._parameter_sliders[index].grid(row=index, column=1, columnspan=3, padx=0, pady=20)
        self._parameter_sliders[index].set(dict_param_and_range[parameter][0].index(current_mode_data[parameter]))
    
        self._parameter_values_label[index].configure(text=f'{dict_param_and_range[parameter][0][dict_param_and_range[parameter][0].index(current_mode_data[parameter])]} {dict_param_and_range[parameter][1]}' if not isinstance(current_mode_data[parameter],str) else f'{current_mode_data[parameter]}')
        self._parameter_values_label[index].grid(row=index, column=5, padx=30, pady=20)

        # updating the value list containing all the most recent data
        self._parameter_value_list[index] = dict_param_and_range[parameter][0][dict_param_and_range[parameter][0].index(current_mode_data[parameter])]
    
    else:
      customtkinter.CTkLabel(master=self, font=font2, text="Select a Mode", text_color=gray_2, anchor="center").grid(row=0,column=0,padx=210, pady=240)

  # sends the list of data to the main class whenever a slider is cahnged
  def _update_changes(self):
    self._send_data_func(self._parameter_value_list)
  