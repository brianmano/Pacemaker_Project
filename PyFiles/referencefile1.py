from tkinter import *
import customtkinter as ctk
from tkinter import font

root = ctk.CTk()
font1 = ctk.CTkFont(family="Lexend", weight="bold", size=20)

fonts=list(font.families())
fonts.sort()
print(fonts)

gray = "#2A2A2A"
blue = "#195FA6"
bg_color = "#1A1A1A"

def response():
    print("hello")

def switch(btn): # toggle button states
    current_state = btn.cget('state')
    new_state = "normal" if current_state == "disabled" else "disabled"
    btn.configure(state=new_state)

root.geometry("1000x700")
root.resizable(False, False)
root.title("Mechtron 3K04")
root.configure(fg_color=bg_color)

frame = ctk.CTkFrame(master=root, width=357, height=601,fg_color=gray, corner_radius=15, border_width=3, border_color=blue)
frame.pack()
frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

button = ctk.CTkButton(master=frame, width = 191, height=43, text="Hello", command=response, font=font1, state="normal")

button.place(relx = 0.5, rely = 0.5, anchor = CENTER)

button2 = ctk.CTkButton(master=frame, width = 191, height=43, text="Toggle", command=lambda: switch(button), font=font1).place(relx = 0.5, rely = 0.6, anchor = CENTER)

root.mainloop()
