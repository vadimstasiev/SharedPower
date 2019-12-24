# please install the following non-standard libraries: bcrypt

import sys
import time
import datetime
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


class uiInterface:
    def __init__(self):
        self.root = Tk()
        self.buffered_user_errors = []
        self.outputed_errors_list = []
        self.user_account = UserClass()

    def run(self):
        self.log_in_ui()

    def log_in_ui(self):
        self.setup_root_frame()
        self.init_default_UI()  # this may not be needed here TODO
        self.root.title("Shared Power - Log in")
        self.add_menu_bar_1()

        __inputPanel = PanedWindow(self.root_frame, orient=HORIZONTAL)
        __inputPanel.grid(row=0, column=1, padx=50, pady=20)

        self.email_input = StringVar()
        self.password_input = StringVar()

        label_text_and_vars = [
            ("Email", self.email_input),
            ("Password", self.password_input),
        ]
        self.generate_ui_label_and_entry(
            label_text_and_vars, __inputPanel, entry_width=40)

        register_label_button = Label(
            __inputPanel, text="Don't have an account? Click to Register", fg="#0400ff")
        register_label_button.bind(
            '<Button-1>', self.goto_register_user_menu)
        register_label_button.grid(row=2, column=1, sticky="e")
        # Button for submit
        submit_button = Button(self.root_frame, text="Log in", command=self.process_log_in).grid(
            column=2, padx=20, pady=20, ipadx=10, ipady=5)
        # Error Message TODO better
        # self.textvar = StringVar()
        # self.error_message_output = Label(
        #     self.root_frame, textvariable=self.textvar, fg="#ff0000").grid(column=1)
        self.root.mainloop()

    def process_log_in(self):
        self.clear_errors()
        __email_address = self.email_input.get()
        __password = self.password_input.get()

        if not (self.user_account.does_email_exist(__email_address)):
            self.buffered_user_errors.append("ERROR - Account not found")
        else:
            self.clear_errors()
            if(self.user_account.check_password(__email_address, __password)):
                __account_user_type = self.user_account.get_user_type()
                if (__account_user_type == "Tool_User"):
                    self.tool_user_options_ui()
                elif (__account_user_type == "Tool_Owner"):
                    self.tool_user_options_ui()  # change to tool owner once that gets added
                else:
                    self.buffered_user_errors.append(
                        "Database Error - Type of User Unknown")
            else:
                self.buffered_user_errors.append("ERROR - Wrong Password")
        self.generate_ui_output_errors(self.root_frame)

    def register_user_ui(self):
        self.setup_root_frame()
        self.init_default_UI()
        self.root.title("Shared Power - Register New User")
        self.add_menu_bar_2()

        self.Label_Frame_Reg = LabelFrame(  # TODO TODO TODO
            self.root_frame, text="Register User")
        self.Label_Frame_Reg.grid(ipadx=50, ipady=30, padx=5, pady=5)
        # __inputPanel = PanedWindow(
        #     self.Label_Frame_Reg, orient=HORIZONTAL)
        # __inputPanel.grid(row=0, column=1, padx=50, pady=20)

        self.first_name_input = StringVar()
        self.surname_input = StringVar()
        self.phone_number_input = StringVar()
        self.post_code_input = StringVar()
        self.home_address_input = StringVar()
        self.email_input = StringVar()
        self.password_input = StringVar()
        self.confirm_password_input = StringVar()

        label_text_and_vars = [  # None = do not generate Entry, useful for different input types
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
        self.generate_ui_label_and_entry(
            label_text_and_vars, self.Label_Frame_Reg)

        self.date_of_birth_entry = DateEntry(
            self.Label_Frame_Reg, width=22, background='darkblue', foreground='white', borderwidth=2)
        self.date_of_birth_entry.grid(row=3, column=1, columnspan=2, sticky=W)
        self.date_of_birth_entry.bind(
            "<<DateEntrySelected>>", self.set_date_of_birth)

        self.user_type = IntVar()
        __radio_buttons_panel = PanedWindow(
            self.Label_Frame_Reg, orient=HORIZONTAL)
        __radio_buttons_panel.grid(row=9, column=1, padx=10, pady=10)
        Radiobutton(self.Label_Frame_Reg, text="Tool User", variable=self.user_type,
                    value=1).grid(row=9, column=1, sticky=W)
        Radiobutton(self.Label_Frame_Reg, text="Tool Owner", variable=self.user_type,
                    value=2).grid(row=9, column=2, sticky=W)

        submit_button = Button(self.Label_Frame_Reg, text="Register", command=self.process_register_new_user).grid(
            column=2, ipadx=10, ipady=5)

        self.root.mainloop()

    def generate_ui_label_and_entry(self, __list, __widget, **kw):
        __label_padx = kw.pop('label_width', 20)
        __entry_width = kw.pop('entry_width', 25)
        for __line in __list:
            label_display, var = __line
            __index = __list.index(__line)
            __label = Label(__widget, text=label_display,
                            padx=__label_padx, pady=3)
            __label.grid(row=__index, sticky=W)
            if var != None:
                __entry = Entry(__widget, width=__entry_width,
                                textvariable=var)
                __entry.grid(row=__index, column=1, columnspan=2, sticky=W)

    def generate_ui_output_errors(self, __widget):
        __buffered_errors = self.get_buffered_user_errors()
        for __line in __buffered_errors:
            __index = __buffered_errors.index(__line) + 99
            # the number 99 is to make sure that it always stays at the bottom
            __label = Label(__widget, text=__line, fg="#ff0000")
            __label.grid(row=__index, column=1)
            self.outputed_errors_list.append(__label)

    def clear_errors(self):
        for __l in self.outputed_errors_list:
            __l.destroy()

    def tool_user_options_ui(self):
        self.setup_root_frame()
        self.root.resizable(width=False, height=False)

        self.add_menu_bar_3()

        panel_1 = PanedWindow(orient=HORIZONTAL).grid()
        # TODO
        Button(panel_1, text="Search for tools", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View current orders", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View Purchase History", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)

        self.root.mainloop()

    def tool_owner_options_ui(self):
        self.setup_root_frame()
        self.root.resizable(width=False, height=False)

        self.add_menu_bar_3()

        panel_1 = PanedWindow(orient=HORIZONTAL).grid()
        # TODO
        Button(panel_1, text="Register tool", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View Listed Inventory", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="Search for tools", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View current orders", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View Purchase History", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="View next Invoice", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)
        Button(panel_1, text="Log Out", width=30).grid(
            ipady=15, padx=20, pady=20, sticky=W)

        self.root.mainloop()

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
        self.generate_ui_output_errors(
            self.Label_Frame_Reg)  # TODO needs more work
        self.log_in_ui()

    def setup_root_frame(self):
        __list = self.get_all_children()
        for __child in __list:
            __child.destroy()
        self.root_frame = Frame(height=2, bd=1, relief=SUNKEN)
        self.root_frame.grid()

    def init_default_UI(self):
        self.root.title("Shared Power")
        self.root.resizable(width=False, height=False)

    def add_menu_bar_1(self):   # used for Login Screen
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Contact Admin",
                              command=self.contact_admin)
        self.menubar.add_cascade(label="Forgot Password", menu=__submenu)
        self.menubar.add_command(label="Quit", command=self.quit)
        self.root.config(menu=self.menubar)

    def add_menu_bar_2(self):   # used for Register Screen
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=self.log_in_ui)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.root.config(menu=self.menubar)

    def add_menu_bar_3(self):   # used for the tool users/owners UI
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Log Out", command=self.log_in_ui)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.root.config(menu=self.menubar)

    def contact_admin(self):
        print("Contact Admin")
        # IDK what to do here, do something fancy lol
        # Can add message inbox to admin's personal db for that stuff, logs, etc
        # Can also create an interface for an admin account

    def menu_search_for_tools(self):
        pass  # TODO

    def menu_view_listed_inventory(self):  # TODO
        print("#"*100)
        __list_results = self.user_account.fetch_user_listed_inventory()
        [print(row) for row in __list_results]
        print("#"*100)

    def menu_view_current_orders(self):
        pass  # TODO

    def menu_view_purchase_history(self):
        pass  # TODO

    def menu_view_next_invoice(self):
        pass  # TODO

    def register_tool(self):  # TODO
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
        pass  # TODO
        # get own tool inventory

    def quit(self):
        self.root.destroy()
        self.root.quit()

    ##### random method for Class functionality #####

    def set_date_of_birth(self, event):
        self.date_of_birth_input = self.date_of_birth_entry.get_date()

    def goto_register_user_menu(self, event):
        self.register_user_ui()

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

    def get_all_children(self):
        __list = self.root.winfo_children()
        for item in __list:
            if item.winfo_children():
                __list.extend(item.winfo_children())
        return __list

    def get_buffered_user_errors(self):
        buffered_errors = tuple(self.buffered_user_errors)
        self.buffered_user_errors.clear()
        return buffered_errors

    ########################################################    Main Program    ###########################################


if __name__ == '__main__':
    program = uiInterface()
    program.run()
