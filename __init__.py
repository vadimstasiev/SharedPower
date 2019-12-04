import enum
import sqlite3
import time
import datetime
import random  # replace this with uuid
from enum import auto
from abc import ABC, abstractmethod, abstractproperty

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccounts import UserDefault, UserType, User_Details_Column_Values

########################################################     Interface    ###########################################


class consoleInterface:

    def __init__(self):
        self.user_account = UserDefault()
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

    def login_menu_and_process(self):
        # Maybe use get the user dictionary here and send off parameters into the other functions
        # self.identify_user()
        __email_address = self.ask_valid_email_address()
        if(self.user_account.update_local_user_info_list(__email_address)):
            print("ERROR - Account NOT FOUND")
            self.menu_first_access()

        if(self.authentificate_user(__email_address)):
            self.menu_tool_owner_account()
        else:
            print("ERROR - Wrong Password")
            self.menu_first_access()

    def register_menu_and_process(self):
        new_user_information = (
            UserDefault.generate_unique_ID(),
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
        self.user_account.register(new_user_information)
        # if(self.user_account.local_user_info_list)

    def menu_tool_owner_account(self):
        print("1: Go to default menu page")
        print("2: Register tool:")
        print("3: Log Out")

        self.print_select_your_option()

        __option = self.get_valid_option(1, 3)
        __switch = {
            1: self.menu_default_user_account,
            2: self.register_tool,
            3: self.escape
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

    def menu_view_current_orders(self):
        print("This is the menu to view the current orders")

    def menu_view_purchase_history(self):
        print("This is the menu to view the purchase history")

    def menu_view_next_invoice(self):
        print("This is the menu to view the next invoice")

    def register_tool(self):
        print("This is the the interface to register a tool")

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

    def ask_user_type(self):
        print("What type of user do you want to register as?")
        print("1: Tool User")
        print("2: Tool Owner - This type allows you to rent out tools and do everything that the tool user can do")
        self.print_select_your_option()
        __option = self.get_valid_option(1, 2)
        __user_type = UserType(__option)
        return str(__user_type)

    def ask_user_password(self):
        __password = input("Please enter your password: ")
        return __password

    def get_hashed_password(self):
        while(True):
            __password = input("Please enter your password(8 - 32 digits): ")
            if 8 <= len(__password) <= 32:
                __password_verify = input("Please verify your password: ")
                if __password_verify == __password:
                    break
        __hashed_password = UserDefault.generate_hashed_password(__password)
        return __hashed_password

    def escape(self):
        # DO Nothing, useful for the workaround switch "statements"
        pass

    ########################################################    Main Program    ###########################################


runInterface = consoleInterface()
# runDatabaseInterface = DatabaseInterface(
#   "This is My database", "value_1", "idkwtf")
