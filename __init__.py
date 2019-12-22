# non-standard libraries: bcrypt

import enum
import sqlite3
import time
import datetime
from enum import auto
from abc import ABC, abstractmethod, abstractproperty

# import tkinter as tk
from tkinter import *

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccounts import UserClass

########################################################     Interface    ###########################################
# Note to self: create another database for "unexpected_DB_changes_log" for instance, when the
# balance is recalculated based on past orders and it doesn't match the balance saved to the profile


class guiInterface:
    def __init__(self):
        self.user_account = UserClass()
        self.log_in_gui()

    def log_in_gui(self):
        self.reset_root()
        self.root.title("Shared Power - Log in")
        self.root.resizable(width=False, height=False)
        menubar = Menu(self.root)
        forgot_password = Menu(menubar, tearoff=0)

        forgot_password.add_command(
            label="Contact Admin", command=self.contact_admin)
        menubar.add_cascade(label="Forgot Password", menu=forgot_password)
        menubar.add_command(label="Quit", command=self.root.quit)

        self.root.config(menu=menubar)

        __inputPanel = PanedWindow(orient=HORIZONTAL)
        __inputPanel.grid(row=0, column=1, padx=50, pady=20)

        Label(__inputPanel, text="Email").grid(row=0, sticky=W)
        Label(__inputPanel, text="Password").grid(row=1, sticky=W)

        self.email_input = Entry(__inputPanel, width=50)
        self.password_input = Entry(__inputPanel, width=50)
        self.email_input.grid(row=0, column=1)
        self.password_input.grid(row=1, column=1)

        register_label_button = Label(
            __inputPanel, text="Don't have an account? Click to Register", fg="#0400ff")
        register_label_button.bind(
            '<Button-1>', self.goto_register_menu)
        register_label_button.grid(row=2, column=1, sticky="e")

        submit_button = Button(self.root, text="Submit", command=self.process_log_in).grid(
            column=2, padx=20, pady=20)
        self.textvar = StringVar()
        self.error_message_output = Label(
            self.root, textvariable=self.textvar, fg="#ff0000").grid(column=1)

        self.root.mainloop()

    def tool_user_options_gui(self):
        self.reset_root()
        self.root.resizable(width=False, height=False)
        menubar = Menu(self.root)
        log_out_menubar = Menu(menubar, tearoff=0)
        log_out_menubar.add_command(
            label="Log Out", command=self.log_in_gui)
        menubar.add_cascade(label="Log Out", menu=log_out_menubar)

        self.root.config(menu=menubar)

        panel_1 = PanedWindow(orient=HORIZONTAL).grid()

        Button(panel_1, text="Search for tools", width=30).grid(
            ipady=15, padx=20, pady=20, sticky="w")
        Button(panel_1, text="View current orders", width=30).grid(
            ipady=15, padx=20, pady=20, sticky="w")
        Button(panel_1, text="View Purchase History", width=30).grid(
            ipady=15, padx=20, pady=20, sticky="w")

        self.root.mainloop()

    def process_log_in(self):
        __email_address = self.email_input.get()
        __password = self.password_input.get()

        if not (self.user_account.does_email_exist(__email_address)):
            self.textvar.set("ERROR - Account NOT FOUND")
        else:
            self.textvar.set("")
            if(self.user_account.check_password(__email_address, __password)):
                __account_user_type = self.user_account.get_user_type()
                if (__account_user_type == "Tool_User"):
                    self.tool_user_options_gui()
                elif (__account_user_type == "Tool_Owner"):
                    self.tool_user_options_gui()
                else:
                    self.textvar.set("Database Error - Type of User Unknown")
            else:
                self.textvar.set("ERROR - Wrong Password")

    def reset_root(self):
        try:
            self.root.destroy()
        except:
            pass
        self.root = Tk()
        self.root.title("Shared Power")

    def contact_admin(self):
        print("Contact Admin")

    def menu_tool_owner_account(self):
        print("1: Register tool")
        print("2: View Listed Inventory")
        print("3: Search for tools")
        print("4: View current orders")
        print("5: View Purchase History")
        print("6: View next Invoice")
        print("7: Log Out")

        self.print_select_your_option()

        __option = self.get_valid_option(1, 7)
        __switch = {
            1: self.register_tool,
            2: self.menu_view_listed_inventory,
            3: self.menu_search_for_tools,
            4: self.menu_view_current_orders,
            5: self.menu_view_purchase_history,
            6: self.menu_view_next_invoice,
            7: self.escape
        }[__option]()

    def menu_default_user_account(self):
        print("1: Search for tools")
        print("2: View current orders")
        print("3: View Purchase History")
        print("4: View next Invoice")
        print("5: Log Out")

        self.print_select_your_option()

        __option = self.get_valid_option(1, 5)
        __switch = {
            1: self.menu_search_for_tools,
            2: self.menu_view_current_orders,
            3: self.menu_view_purchase_history,
            4: self.menu_view_next_invoice,
            5: self.escape
        }[__option]()

    def menu_search_for_tools(self):
        print("This is the search menu")

    def menu_view_listed_inventory(self):
        print("#"*100)
        __list_results = self.user_account.fetch_user_listed_inventory()
        [print(row) for row in __list_results]
        print("#"*100)

    def menu_view_current_orders(self):
        print("This is the menu to view the current orders")

    def menu_view_purchase_history(self):
        print("This is the menu to view the purchase history")

    def menu_view_next_invoice(self):
        print("This is the menu to view the next invoice")

    def goto_register_menu(self, event):
        self.register_menu_and_process()

    def register_menu_and_process(self):
        self.user_account.register(
            UserClass.generate_unique_ID(),
            input("Please enter your first name: "),
            input("Please enter your surname: "),
            self.ask_valid_date_of_birth(),
            self.ask_phone_number(),
            input("Please enter your home address: "),
            input("Please enter your post code: "),
            self.ask_valid_email_address(),
            self.get_hashed_password(),
            0,                                           # Outstanding Balance
            self.ask_user_type()
        )
        self.log_in_gui()

    def register_tool(self):
        # new_tool
        self.user_account.register_tool(
            UserClass.generate_unique_ID(),
            input("Please enter the item name: "),
            self.get_valid_price("Please enter the half-day fee: "),
            self.get_valid_price("Please enter the full-day fee: "),
            input("Please enter the tool description: "),
            input("Please enter the availability of the tool: "),
        )
        self.menu_tool_owner_account()

    def view_own_tool_inventory(self):
        print("This is the the interface to view the tool inventory")
        # get own tool inventory

    ##### Class method functionality #####

    def print_select_your_option(self):
        print("Select your option: ", end=" ")

    def get_valid_integer(self):
        while(True):
            try:
                __consoleInput = int(input())
                break
            except:
                print("Please enter an integer number.")
        return __consoleInput

    def get_valid_option(self, __x, __y):
        while(True):
            option1 = self.get_valid_integer()
            if(__x <= option1 <= __y):
                break
        return option1

    def get_hashed_password(self):
        while(True):
            __password = input("Please enter your password(8 - 32 digits): ")
            if 8 <= len(__password) <= 32:
                __password_verify = input("Please verify your password: ")
                if __password_verify == __password:
                    break
        __hashed_password = UserClass.generate_hashed_password(__password)
        return __hashed_password

    def get_valid_price(self, __text: str):
        __price = 0
        while(True):
            try:
                __price = int(input(__text)) * 100
                break
            except:
                print("Please enter correct price format e.g.: £20.00")
        return __price

    def get_unix_timestamp(self):
        return int(time.time())

    def ask_valid_date_of_birth(self):
        try:
            print("Please enter your date of birth:")
            print("Day(1 - 31): ", end=" ")
            __day = self.get_valid_option(1, 31)
            print("Month(1 - 12): ", end=" ")
            __month = self.get_valid_option(1, 12)
            print(f"Year(1910 - {str(datetime.date.today().year)}): ", end=" ")
            __year = self.get_valid_option(1900, datetime.date.today().year)
            __date_of_birth = datetime.datetime(__year, __month, __day)
            date_of_birth_str = __date_of_birth.strftime("%D")
        except:
            print("Error - The date entered is invalid")
            date_of_birth_str = self.ask_valid_date_of_birth()
        return date_of_birth_str

    def ask_phone_number(self):
        print("Please enter your phone number: ", end=" ")
        return self.get_valid_integer()

    def ask_valid_email_address(self):
        while(True):
            __email_address = input("Please enter your email address: ")
            if(__email_address.find("@") != -1):
                break
        return __email_address

    def ask_valid_email_address_not_in_DB(self):
        while(True):
            __email_address = self.ask_valid_email_address()
            if not self.user_account.does_email_exist(__email_address):
                break
            else:
                print("Email already taken please choose a different one.")

    def ask_user_type(self):
        print("As what type of user do you want to register?")
        print("1: Tool User")
        print("2: Tool Owner - This will require proof of residency and approval")
        self.print_select_your_option()
        __option = self.get_valid_option(1, 2)
        __user_type = {
            1: "Tool_User",
            2: "Tool_Owner",
        }[__option]
        return __user_type

    def ask_user_password(self):
        __password = input("Please enter your password: ")
        return __password

    def escape(self):
        # DO Nothing, useful for the workaround "switch statements"
        pass

    ########################################################    Main Program    ###########################################


runInterface = guiInterface()
