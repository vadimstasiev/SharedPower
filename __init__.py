# non-standard libraries: bcrypt

import time
import datetime

# import tkinter as tk
from tkinter import *

# Import local downloaded classes
from ImportedClasses.calendar_ import *
from ImportedClasses.dateentry import *


# Import local classes
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccounts import UserClass

########################################################     Interface    ###########################################
# Note to self: create another database for "unexpected_DB_changes_log" for instance, when the
# balance is recalculated based on past orders and it doesn't match the balance saved to the profile


class guiInterface:
    def __init__(self):
        self.buffered_user_errors = []
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

        __inputPanel = PanedWindow(self.root, orient=HORIZONTAL)
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
            '<Button-1>', self.goto_register_user_menu)
        register_label_button.grid(row=2, column=1, sticky="e")

        submit_button = Button(self.root, text="Log in", command=self.process_log_in).grid(
            column=2, padx=20, pady=20, ipadx=10, ipady=5)
        self.textvar = StringVar()
        self.error_message_output = Label(
            self.root, textvariable=self.textvar, fg="#ff0000").grid(column=1)

        self.root.mainloop()

    def register_user_gui(self):
        self.reset_root()
        self.root.title("Shared Power - Register New User")
        self.root.resizable(width=False, height=False)
        menubar = Menu(self.root)
        options = Menu(menubar, tearoff=0)

        options.add_command(label="Go Back", command=self.log_in_gui)
        options.add_command(label="Quit", command=self.root.quit)
        menubar.add_cascade(label="Options", menu=options)
        self.root.config(menu=menubar)

        self._label_frame_register = LabelFrame(
            self.root, text="Register User")
        self._label_frame_register.grid(ipadx=50, ipady=30, padx=5, pady=5)
        __inputPanel = PanedWindow(
            self._label_frame_register, orient=HORIZONTAL)
        __inputPanel.grid(row=0, column=1, padx=50, pady=20)

        self.first_name_input = StringVar()
        self.surname_input = StringVar()
        self.phone_number_input = StringVar()
        self.post_code_input = StringVar()
        self.home_address_input = StringVar()
        self.email_input = StringVar()
        self.password_input = StringVar()
        self.confirm_password_input = StringVar()

        new_labels_display = [
            ("First Name", self.first_name_input),
            ("Surname", self.surname_input),
            ("Phone Number", self.phone_number_input),
            ("Date of Birth", None),
            ("Post Code", self.post_code_input),
            ("Home Address", self.home_address_input),
            ("Email", self.email_input),
            ("Password", self.password_input),
            ("Confirm Password", self.confirm_password_input),
            ("User Type", None)
        ]

        for __line in new_labels_display:
            label_display, var = __line
            __index = new_labels_display.index(__line)
            __label = Label(__inputPanel, text=label_display, padx=20, pady=3)
            __label.grid(row=__index, sticky=W)
            if var != None:
                __entry = Entry(__inputPanel, width=25, textvariable=var)
                __entry.grid(row=__index, column=1, columnspan=2, sticky=W)

        self.date_of_birth_entry = DateEntry(
            __inputPanel, width=22, background='darkblue', foreground='white', borderwidth=2)
        self.date_of_birth_entry.grid(row=3, column=1, columnspan=2, sticky=W)
        self.date_of_birth_entry.bind(
            "<<DateEntrySelected>>", self.set_date_of_birth)

        self.user_type = IntVar()
        __radio_buttons_panel = PanedWindow(__inputPanel, orient=HORIZONTAL)
        __radio_buttons_panel.grid(row=9, column=1, padx=10, pady=10)
        Radiobutton(__inputPanel, text="Tool User", variable=self.user_type,
                    value=1).grid(row=9, column=1, sticky=W)
        Radiobutton(__inputPanel, text="Tool Owner", variable=self.user_type,
                    value=2).grid(row=9, column=2, sticky=W)

        submit_button = Button(self._label_frame_register, text="Register", command=self.process_register_new_user).grid(
            column=2, ipadx=10, ipady=5)
        self.textvar = StringVar()

        self.error_message_output = Label(
            self._label_frame_register, textvariable=self.textvar, fg="#ff0000")
        self.error_message_output.grid(column=1)

        self.root.mainloop()

    def register_user_gui_output_errors(self):
        __buffered_errors = self.get_buffered_user_errors()
        for __line in __buffered_errors:
            __index = __buffered_errors.index(__line) + 99
            # the number 99 is to make sure that it always stays at the bottom
            __label = Label(self._label_frame_register,
                            text=__line, fg="#ff0000")
            __label.grid(row=__index, column=1)

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
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View current orders", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View Purchase History", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)

        self.root.mainloop()

    def process_log_in(self):
        __email_address = self.email_input.get()
        __password = self.password_input.get()

        if not (self.user_account.does_email_exist(__email_address)):
            self.textvar.set("ERROR - Account not found")
        else:
            self.textvar.set("")
            if(self.user_account.check_password(__email_address, __password)):
                __account_user_type = self.user_account.get_user_type()
                if (__account_user_type == "Tool_User"):
                    self.tool_user_options_gui()
                elif (__account_user_type == "Tool_Owner"):
                    self.tool_user_options_gui()  # change to tool owner once that gets added
                else:
                    self.textvar.set("Database Error - Type of User Unknown")
            else:
                self.textvar.set("ERROR - Wrong Password")

    def process_register_new_user(self):  # TODO
        __valid_email_address = self.get_valid_email_address()
        __password_hash = self.get_valid_hashed_password()
        self.textvar.set("")
        self.user_account.register(
            UserClass.generate_unique_ID(),
            str(self.first_name_input.get()),
            str(self.surname_input.get()),
            self.date_of_birth_input,
            int(self.phone_number_input.get()),
            str(self.home_address_input.get()),
            str(self.post_code_input.get()),
            __valid_email_address,
            __password_hash,
            0,                                           # Outstanding Balance
            "Tool_User" if self.user_type.get() == 1 else "Tool_Owner"
        )
        self.register_user_gui_output_errors()  # TODO needs more work
        self.log_in_gui()

    def reset_root(self):
        try:
            self.root.destroy()
        except:
            pass
        self.root = Tk()
        self.root.title("Shared Power")

    def contact_admin(self):
        print("Contact Admin")
        # IDK what to do here, do something fancy lol
        # Can add message inbox to admin's personal db for that stuff, logs, etc
        # Can also create an interface for an admin account

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
        pass    # done this: self.tool_user_options_gui

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

    def set_date_of_birth(self, event):
        self.date_of_birth_input = self.date_of_birth_entry.get_date()

    def goto_register_user_menu(self, event):
        self.register_user_gui()

    def get_valid_hashed_password(self):
        __password = self.password_input.get()
        if(__password == self.confirm_password_input.get()):
            if 8 <= len(__password) <= 32:
                __hashed_password = UserClass.generate_hashed_password(
                    __password)
            else:
                self.textvar.set("Please enter a password w/ 8 - 32 digits")
                __hashed_password = None
        else:
            self.textvar.set("ERROR - Passwords do not match")
        return __hashed_password

    def get_valid_email_address(self):
        __email = self.email_input.get()
        if self.user_account.does_email_exist(__email):
            self.textvar.set("ERROR - Email Already Exists")
            __email = None
        return __email

    def get_unix_timestamp(self):
        return int(time.time())

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

    def get_buffered_user_errors(self):
        buffered_errors = tuple(self.buffered_user_errors)
        self.buffered_user_errors.clear()
        return buffered_errors

    ########################################################    Main Program    ###########################################


if __name__ == '__main__':
    runInterface = guiInterface()
