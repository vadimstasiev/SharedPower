# non-standard libraries: bcrypt

import enum
import sqlite3
import time
import datetime
import random  # replace this with uuid
from enum import auto
from abc import ABC, abstractmethod, abstractproperty

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccounts import UserClass

########################################################     Interface    ###########################################
# Note to self: create another database for "unexpected_DB_changes_log" for instance, when the
# balance is recalculated based on past orders and it doesn't match the balance saved to the profile


class consoleInterface:

    def __init__(self):
        self.user_account = UserClass()
        self.menu_first_access()

    def menu_first_access(self):
        print("1:Log in")
        print("2:Register")
        print("3:Exit")
        self.print_select_your_option()

        __option = self.get_valid_option(1, 3)
        __switch = {
            1: self.login_menu_and_process,
            2: self.register_menu_and_process,
            3: self.escape
        }[__option]()

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

    def login_menu_and_process(self):
        __email_address = self.ask_valid_email_address()

        if not (self.user_account.does_email_exist(__email_address)):
            print("ERROR - Account NOT FOUND")
            self.menu_first_access()
        else:
            # sessionID
            if(self.authentificate_user(__email_address)):
                __account_user_type = self.user_account.get_user_type()
                if (__account_user_type == "Tool_User"):
                    self.menu_default_user_account()
                elif (__account_user_type == "Tool_Owner"):
                    self.menu_tool_owner_account()
                else:
                    print("Error - Type of User Unknown")
            else:
                print("ERROR - Wrong Password")
        self.menu_first_access()

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
        self.menu_first_access()

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

    def authentificate_user(self, __email_address):
        return self.user_account.check_password(__email_address, self.ask_user_password())

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


runInterface = consoleInterface()
