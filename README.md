# PACEMAKER UI - MECHTRON 3K04

## Environment and Libraries
- Python3
- TKinter
- customtkinter

## Git

Please use GIT to maintain version control

### Clone repository
clone the repository onto your local device and edit on that

### Branches
When pulling from the repository, create your own branch and work on that branch; do not work on the main branch.

### Pull requests/commits
Use ```git add .```, ```git commit -m "Insert commit msg here"``` and ```git push . ``` to push the changes onto the repository. When writing comments for git commit, please keep them short and descriptive. **DO NOT** copy your code, paste it into GitHub, and commit your code in that manner.

## Coding Conventions

### Class Structure:
- Define classes in a separate .py file and **NOT** within the main_app.py file unless it is the main app class loop
  - You can call the other classes by adding the following line to the top of the class
    ``` py
    from <file_name> import <class_name>
    ```
### Variable Naming:
- For Tkinter variables, name them appropriately based on the type of object it is (ie. button, frames, etc), where in the app it is supposed to be located (ie. welcome screen, main interface), and what the button is meant to represent
  - Example: Sign In button on welcome screen --> btn_welcome_signin

    
    **Naming Convention Table:**
    Tkinter Object  | Variable Prefix
    --------------- | ---------------
    Button     | btn
    Frame      | frm
    Window     | win
    Scroll Bar | sb
    Label      | lbl
- For other generic variables that are not objects, include the datatype of the variable within the variable name and what it is meant to do
  - Example: integer counter --> Variable Name: int_counter
  - Example: string username --> Variable Name: str_username
 
    **Naming Convention Table:**
    Type  | Variable Prefix
    --------------- | ---------------
    Integer     | int
    String      | str
    Boolean     | bool
    Float       | flt
    List        | lst

### Using CustomTkinter:
- When creating objects in customtkinter and passing in arguments for the object (Ex. root, text, etc), please include the variable of the argument. Ex.
  ```py
  btn_welcome_signin = customtkinter.CTkButton(master=root, width = 191, height=43, text="Sign In", command=response, font=font1)
  ```
  **NOT**
  ```py
  btn_welcome_signin = customtkinter.CTkButton(mroot, 191, 43, "Sign In", response, font1)
  ```
### Comments:
PLEASE COMMENT EVERYTHING FOR CODE YOU WRITE - it will be easier to follow along with what you did and how you did it
