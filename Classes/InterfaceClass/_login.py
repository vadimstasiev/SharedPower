import sys
import time
import datetime
import uuid
import os
import shutil
from tkinter import *
from tkinter import messagebox
from typing import List

# Import local classes
from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
from Classes.tkinterwidgets.getfileswidget import GetFilesWidget, GetImagesWidget, DisplayImagesWidget
from Classes.tkinterwidgets.calendar_ import Calendar
from Classes.tkinterwidgets.dateentry import DateEntry
from Classes.MoneyParser import price_str, price_dec
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
from Classes.UserClass import UserClass
from Classes.ToolClass import ToolClass


def log_in_UI(self, **kw):
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - Log in")
    self.add_menu_bar_UI_1()
    # Parent
    PWparent = PanedWindow(self.root_frame, orient=HORIZONTAL)
    PWparent.grid(row=0, column=1, padx=50, pady=20)
    # StrVars
    email_StrVar = StringVar()
    password_StrVar = StringVar()
    # Labels and Entries
    self.generate_labels_and_entries_UI(
        PWparent, [
            ("Email: ", email_StrVar),
            ("Password: #{type=pw", password_StrVar),
        ], entry_width=40)
    # Register Button
    registerB = Label(
        PWparent,
        text="Don't have an account? Click to Register",
        fg="#0400ff"
    )

    def goto_register_user(event):
        self.register_user_UI()
    registerB.bind('<Button-1>', goto_register_user)
    registerB.grid(row=2, column=1, sticky="e")
    # Button for submittion
    loginB = Button(
        PWparent,
        text="Log in",
        command=self.process_log_in)
    loginB.grid(column=2, padx=20, pady=20, ipadx=10, ipady=5)
    # Class Variables
    self.email = email_StrVar
    self.password = password_StrVar
    # Bind return key

    def Return_keypressed(event):
        self.process_log_in()
    self.root.bind('<Return>', Return_keypressed)
    # Generate any already existent errors
    self.generate_output_errors_UI(PWparent, starting_index=100)
    # This is usefull for automatic login:
    if len(kw) > 0:
        email_StrVar.set(kw.get('email', ''))
        password_StrVar.set(kw.get('password', ''))
        self.process_log_in()
    self.root.mainloop()


def process_log_in(self, **kw):
    email, password = self.email.get(), self.password.get()
    self.clear_errors()
    if not (self.user_instance.does_email_exist(email)):
        self.buffered_errors.append("Account not found")
    else:
        if(self.user_instance.check_password(email, password)):
            self.menu_user_options_UI()
        else:
            self.buffered_errors.append("Wrong Password")
    self.generate_output_errors_UI(self.root_frame, starting_index=100)
