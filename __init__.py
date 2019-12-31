# please install the following non-standard libraries: bcrypt, Pillow?(not sure if actually needed) , Babel, tkcalendar

import sys
import time
import datetime
from tkinter import *

# Import local classes
from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
from Classes.tkinterwidgets.getfileswidget import GetFilesWidget
from Classes.tkinterwidgets.calendar_ import Calendar
from Classes.tkinterwidgets.dateentry import DateEntry
from Classes.MoneyParser import price_str, price_dec
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccounts import UserClass

########################################################     Interface    ###########################################
# Note to self: create another database for "unexpected_DB_changes_log" for instance, when the
# balance is recalculated based on past orders and it doesn't match the balance saved to the profile


class uiInterface:
    def __init__(self):
        self.UI_root = Tk()
        self.buffered_user_errors = []
        self.outputed_errors_list = []
        self.user_account = UserClass()

        self.image_filetypes = [
            ('Image files', '*.png'),
        ]

    def run(self):
        self.log_in_ui()

    def log_in_ui(self, **kw):
        self.setup_new_window()
        self.init_default_UI()
        self.UI_root.title("Shared Power - Log in")
        self.add_menu_bar_1()

        __inputPanel = PanedWindow(self.UI_root_frame, orient=HORIZONTAL)
        __inputPanel.grid(row=0, column=1, padx=50, pady=20)

        self.email_TKentry = StringVar()
        self.password_TKentry = StringVar()

        label_text_and_vars = [
            ("Email: ", self.email_TKentry),
            ("Password: #{type=pw", self.password_TKentry),
        ]
        self.generate_ui_label_and_entry(
            __inputPanel, label_text_and_vars, entry_width=40)
        if len(kw)>0:
            self.email_TKentry.set(kw.get('email', ''))
            self.password_TKentry.set(kw.get('password', ''))

        register_label_button = Label(
            __inputPanel, text="Don't have an account? Click to Register", fg="#0400ff")
        register_label_button.bind(
            '<Button-1>', self.goto_register_user_menu)
        register_label_button.grid(row=2, column=1, sticky="e")


        # Button for submittion
        Button(self.UI_root_frame, text="Log in", command=self.process_log_in).grid(
            column=2, padx=20, pady=20, ipadx=10, ipady=5)
        #Bind return key
        def Return_keypressed(event):
            self.process_log_in()
        self.UI_root.bind('<Return>', Return_keypressed)
        self.UI_root.mainloop()

    def process_log_in(self, **kw):
        self.clear_errors()
        __email_address = self.email_TKentry.get()
        __password = self.password_TKentry.get()
        if not (self.user_account.does_email_exist(__email_address)):
            self.buffered_user_errors.append("Account not found")
        else:
            if(self.user_account.check_password(__email_address, __password)):
                __account_user_type = self.user_account.get_user_type()
                if (__account_user_type == "Tool_User"):
                    self.tool_user_options_ui()
                elif (__account_user_type == "Tool_Owner"):
                    self.tool_owner_options_ui()
                else:
                    self.buffered_user_errors.append(
                        "Database Error - Type of User Unknown")
            else:
                self.buffered_user_errors.append("Wrong Password")
        self.generate_ui_output_errors(self.UI_root_frame, starting_index=100)

    def register_user_ui(self):
        self.setup_new_window()
        self.init_default_UI()
        self.UI_root.title("Shared Power - Register New User")
        self.add_menu_bar_2()

        self.Label_Frame_Reg = self.add_label_frame(
            self.UI_root_frame, "Register User", ipadx=50, ipady=30, padx=5, pady=5)

        self.first_name_TKentry = StringVar()
        self.surname_TKentry = StringVar()
        self.phone_number_TKentry = StringVar()
        self.post_code_TKentry = StringVar()
        self.home_address_TKentry = StringVar()
        self.email_TKentry = StringVar()
        self.password_TKentry = StringVar()
        self.confirm_password_TKentry = StringVar()

        label_text_and_vars = [  # None = do not generate Entry, useful for different input widgets
            ("First Name: ", self.first_name_TKentry),
            ("Surname: ", self.surname_TKentry),
            ("Phone Number: ", self.phone_number_TKentry),
            ("Date of Birth: ", None),
            ("Post Code: ", self.post_code_TKentry),
            ("Home Address:", self.home_address_TKentry),
            ("Email: ", self.email_TKentry),
            ("Password: #{type=pw", self.password_TKentry),
            ("Confirm Password: #{type=pw", self.confirm_password_TKentry),
            ("User Type: ", None)
        ]
        self.generate_ui_label_and_entry(
            self.Label_Frame_Reg, label_text_and_vars)

        # Custom calendar input widget
        self.birthday_dateStrVar = StringVar()
        self.add_date_entry(
            self.Label_Frame_Reg, self.birthday_dateStrVar, row=3, column=1, columnspan=2, sticky=W)

        self.user_type_IntVar = self.add_two_radio_buttons_get_var(
            self.Label_Frame_Reg, "Tool User", "Tool Owner", row=9, sticky=W)

        submit_button = Button(self.Label_Frame_Reg, text="Register", command=self.process_register_new_user)
        submit_button.grid(column=2, ipadx=10, ipady=5)


        def Return_keypressed(event):
            self.process_register_new_user()
        self.UI_root.bind('<Return>', Return_keypressed)
        self.UI_root.mainloop()

    def process_register_new_user(self):
        self.clear_errors()
        self.validate_register_user_input()

        if(len(self.buffered_user_errors) == 0):
            self.user_account.register(
                first_name=self.reg_U_first_name,
                surname=self.reg_U_surname,
                bithday=self.reg_U_birthday_date,
                phone_number=self.reg_U_phone_number,
                home_address=self.reg_U_home_address,
                post_code=self.reg_U_post_code,
                email=self.reg_U_email,
                password=self.reg_U_password,
                user_type = "Tool_User" if self.reg_U_user_type == 1 else "Tool_Owner"
            )
            self.log_in_ui()
        else:
            self.generate_ui_output_errors(
                self.Label_Frame_Reg, column=3, padx=50,  sticky=SE)
    def validate_register_user_input(self):
        self.reg_U_first_name = str(self.first_name_TKentry.get())
        self.reg_U_surname = str(self.surname_TKentry.get())
        self.reg_U_birthday_date = str(self.birthday_dateStrVar.get())
        self.reg_U_home_address = str(self.home_address_TKentry.get())
        self.reg_U_post_code = str(self.post_code_TKentry.get())
        self.reg_U_email = str(self.email_TKentry.get())
        self.reg_U_password = str(self.password_TKentry.get())
        self.reg_U_confirm_password = self.confirm_password_TKentry.get()
        self.reg_U_user_type = int(self.user_type_IntVar.get())

        if(self.reg_U_first_name == ""):
            self.buffered_user_errors.append("Please enter your first name")
        if(self.reg_U_surname == ""):
            self.buffered_user_errors.append("Please enter your surname")
        if self.user_account.does_email_exist(self.reg_U_email):
            self.buffered_user_errors.append("Email already exists")
        if (self.reg_U_email.find("@") == -1):
            self.buffered_user_errors.append("Please enter a valid email")
        try:
            __numberStr = self.phone_number_TKentry.get()
            if __numberStr == "":
                self.buffered_user_errors.append("Please enter a phone number")
            self.reg_U_phone_number = int(__numberStr)
        except:
            self.buffered_user_errors.append("Please enter a valid phone number")
        if self.reg_U_birthday_date == datetime.datetime.now().strftime('%d/%m/%Y'):
            self.buffered_user_errors.append("Please enter a valid date")
        if(self.reg_U_post_code == ""):
            self.buffered_user_errors.append("Please enter your postcode")
        if(self.reg_U_home_address == ""):
            self.buffered_user_errors.append("Please enter your home address")
        if not (self.reg_U_password == self.reg_U_confirm_password):
            self.buffered_user_errors.append("Passwords do not match")
        if not 8 <= len(self.reg_U_password) <= 32:
            self.buffered_user_errors.append("Please enter a password w/ 8 - 32 digits")
        if (self.reg_U_user_type == 0):
            self.buffered_user_errors.append("Please select the type of account")

    def register_tool_ui(self):
        self.setup_new_window()
        self.init_default_UI()
        self.UI_root.title("Shared Power - Register New Tool")
        self.add_menu_bar_4()

        self.Label_Frame_Reg = self.add_label_frame(
            self.UI_root_frame, "Register Tool", ipadx=50, ipady=30, padx=5, pady=5)

        self.tool_name = StringVar()
        self.half_day_rate = StringVar()
        self.full_day_rate = StringVar()
        self.post_code_TKentry = StringVar()
        self.home_address_TKentry = StringVar()

        label_text_and_vars = [  # None = do not generate Entry, useful for different input widgets
            ("Tool Name: ", self.tool_name),
            ("Description: ", None),
            ("Half day rate: ", self.half_day_rate),
            ("Full Day Rate: ", self.full_day_rate),
            ("Availablity start date: ", None),
            ("Availablity end date: ", None),
            ("Choose Photo: ", None),

        ]
        self.generate_ui_label_and_entry(
            self.Label_Frame_Reg, label_text_and_vars)
        self.description_text_box = Text(
            self.Label_Frame_Reg, wrap=WORD, height=10, width=80)
        self.description_text_box.grid(row=1, column=1, columnspan=5)

        # Custom calendar input widget
        self.availability_start_date_StrVar = StringVar()
        self.add_date_entry(
            self.Label_Frame_Reg, self.availability_start_date_StrVar, row=4, column=1, columnspan=2, sticky=W)
        self.availability_end_date_StrVar = StringVar()
        self.add_date_entry(
            self.Label_Frame_Reg, self.availability_end_date_StrVar, row=5, column=1, columnspan=2, sticky=W)
        self.file_name = ''

        
        files_widget = GetFilesWidget(self.Label_Frame_Reg, empty_message='Add Photo', file_types=self.image_filetypes, max_items=5)
        files_widget.grid(row=6, column=1, columnspan=2, sticky=W)

        Button(self.Label_Frame_Reg, text="Register", command=self.process_register_new_tool).grid(
            column=5, ipadx=10, ipady=5)
        


        self.UI_root.mainloop()

    def process_register_new_tool(self):  # TODO TODO TODO
        self.validate_register_tool_input()

        if(len(self.buffered_user_errors) == 0):
            self.clear_errors()
            self.user_account.register_tool(
                item_name=self.reg_T_tool_name,
                half_day_fee=self.get_savable_int_price(self.reg_T_half_day_rate),
                full_day_fee=self.get_savable_int_price(self.reg_T_full_day_rate),
                description=self.reg_T_description,
                availability=self.get_packed_availability_dates(),
                photos=0 # hopefully all photos can be packed inside of this
            )
            self.current_menu()
        else:
            self.clear_errors()
            self.generate_ui_output_errors(
                self.Label_Frame_Reg, column=0, starting_index=100, padx=50,  sticky=SE)

    def validate_register_tool_input(self):
        self.reg_T_tool_name = str(self.tool_name.get())
        self.reg_T_description = str(self.description_text_box.get("1.0", 'end-1c'))
        self.reg_T_half_day_rate = str(self.half_day_rate.get())
        self.reg_T_full_day_rate = str(self.full_day_rate.get())
        self.reg_T_availability_list = []
        self.reg_T_availability_list.append(str(self.availability_start_date_StrVar.get()))
        self.reg_T_availability_list.append(str(self.availability_end_date_StrVar.get()))

        if(self.reg_T_tool_name == ""):
            self.buffered_user_errors.append(
                "Please enter the tool name")
        if(self.reg_T_description == ""):
            self.buffered_user_errors.append(
                "Please enter a description")

        if self.reg_T_half_day_rate == 0:
            self.buffered_user_errors.append(
                "Please enter the half day rate")
        try: # TODO
            float(self.reg_T_half_day_rate)
        except:
            self.buffered_user_errors.append(
                "Please enter a valid price for the half day rate")

        if self.reg_T_full_day_rate == 0:
            self.buffered_user_errors.append(
                "Please enter the full day rate")
        try:
            float(self.reg_T_full_day_rate)
        except:
            self.buffered_user_errors.append(
                "Please enter a valid price for the full day rate")
        # if self.reg_T_availability_start_date == datetime.datetime.now().strftime('%d/%m/%Y'):
        #     self.buffered_user_errors.append(
        #         "Please Enter a Valid Date")

    def get_packed_availability_dates(self):
        __list = self.reg_T_availability_list
        __reg_T_availability_str_pack = __list[0]
        for __date in __list:
            __reg_T_availability_str_pack += '#' + __date
        return __reg_T_availability_str_pack

    def get_unpacked_dates(self, __dates_str_packed: str):
        __list = __dates_str_packed.split('#')
        return __list

    def generate_ui_label_and_entry(self, __widget, __list, **kw):
        __label_padx = kw.pop('label_width', 20)
        __entry_width = kw.pop('entry_width', 25)

        str_keywords = [
            "{type=pw",
        ]

        for __line in __list:
            label_display, var = __line
            __index = __list.index(__line)
            __property = ""
            if(label_display.find("#") != -1):
                for i in str_keywords:
                    label_display = label_display.strip(i)
                    __property = i
                label_display = label_display.strip("#")
            __label = Label(__widget, text=label_display,
                            padx=__label_padx, pady=3)
            __label.grid(row=__index, sticky=NW)
            if var != None:
                entry_dic = {}
                entry_dic['width'] = __entry_width
                entry_dic['textvariable'] = var

                # Apply the right properties
                if(__property == "{type=pw"):
                    entry_dic['show'] = "*"
                    __entry = Entry(__widget, entry_dic)
                else:
                    __entry = Entry(__widget, entry_dic)
                __entry.grid(row=__index, column=1, columnspan=2, sticky=W)

    def generate_ui_output_errors(self, __widget, **kw):
        __buffered_errors = self.get_buffered_user_errors()
        __start_on = kw.pop('starting_index', 0)
        for __line in __buffered_errors:
            __index = __buffered_errors.index(__line) + __start_on
            __label = Label(__widget, text=__line, fg="#ff0000")
            if len(kw) == 0:
                __label.grid(row=__index, column=1)
            else:
                kw['row'] = __index
                __label.grid(kw)

            self.outputed_errors_list.append(__label)

    def generate_ui_functions_menu(self, __widget, __list, **kw):
        __label_padx = kw.pop('label_width', 20)
        __entry_width = kw.pop('entry_width', 25)
        for __line in __list:
            __text, function = __line

            if function != None:
                __button = Button(__widget, text=__text,
                                  width=30, command=function)
            else:
                __button = Button(__widget, text=__text, width=30)

            if len(kw) == 0:
                __button.grid(ipady=15, padx=20, pady=20, sticky=W)
            else:
                __button.grid(kw)

    def add_date_entry(self, __widget, __var, **kw):
        __date_entry = DateEntry(__widget, width=22, background='darkblue',
                                 foreground='white', textvariable=__var, date_pattern='d/m/yyyy', borderwidth=2)
        __date_entry.grid(kw)
        return __date_entry

    def add_label_frame(self, __widget, __text, **kw):
        __label_frame = LabelFrame(__widget, text=__text)
        __label_frame.grid(kw)
        return __label_frame

    def add_two_radio_buttons_get_var(self, __widget, __textB1, __textB2, **kw):
        __user_type_input = IntVar()
        __radio_button1 = Radiobutton(self.Label_Frame_Reg, text="Tool User", variable=__user_type_input,
                                      value=1)
        __radio_button2 = Radiobutton(self.Label_Frame_Reg, text="Tool Owner", variable=__user_type_input,
                                      value=2)
        kw['column'] = 1
        __radio_button1.grid(kw)
        kw['column'] = 2
        __radio_button2.grid(kw)
        return __user_type_input

    def clear_errors(self):
        for __l in self.outputed_errors_list:
            __l.destroy()

    def tool_user_options_ui(self):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)

        self.current_menu = self.tool_user_options_ui

        self.add_menu_bar_3()

        button_text_and_functions = [
            ("Search for tools", None),
            ("View current orders", None),
            ("View next Invoice", None),
            ("Log Out", self.log_in_ui),
        ]

        self.generate_ui_functions_menu(
            self.UI_root_frame, button_text_and_functions)

        self.UI_root.mainloop()

    def tool_owner_options_ui(self):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)

        self.current_menu = self.tool_owner_options_ui

        self.add_menu_bar_3()

        button_text_and_functions = [
            ("Register tool", self.register_tool_ui),
            ("View Listed Inventory", self.menu_view_listed_inventory),
            ("Search for tools", None),
            ("View current orders", None),
            ("View Purchase History", None),
            ("View next Invoice", None),
            ("Log Out", self.log_in_ui),
        ]

        self.generate_ui_functions_menu(
            self.UI_root_frame, button_text_and_functions)

        self.UI_root.mainloop()

    def setup_new_window(self):
        self.UI_root.resizable(width=True, height=True)
        self.UI_root.minsize(0, 0)
        self.UI_root.unbind('<Return>')
        __list = self.get_all_children()
        for __child in __list:
            __child.destroy()
        self.UI_root_frame = Frame(self.UI_root, height=2, bd=1, relief=SUNKEN)
        self.UI_root.geometry("")
        self.UI_root_frame.grid()

    def init_default_UI(self):
        self.UI_root.title("Shared Power")
        self.UI_root.resizable(width=False, height=False)

    def add_menu_bar_1(self):   # used for Login Screen
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Contact Admin",
                              command=self.contact_admin)
        self.menubar.add_cascade(label="Forgot Password", menu=__submenu)
        self.menubar.add_command(label="Quit", command=self.quit)
        self.UI_root.config(menu=self.menubar)

    def add_menu_bar_2(self):   # used for Register Screen
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=self.log_in_ui)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)

    def add_menu_bar_3(self):   # used for the tool users/owners UI
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Log Out", command=self.log_in_ui)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)

    def add_menu_bar_4(self):   # used for the sub pages of the tool users/owners UI
        __user_type = self.user_account.get_user_type()
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=self.run_current_menu)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)

    def contact_admin(self):
        print("Contact Admin")
        # IDK what to do here, do something fancy lol
        # Can add message inbox to admin's personal db for that stuff, logs, etc
        # Can also create an interface for an admin account

    def menu_search_for_tools(self):
        pass  # TODO

    def menu_view_listed_inventory(self):  # TODO
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=True)
        self.UI_root.title("Shared Power - View Stock Inventory")
        self.add_menu_bar_4()
        self.UI_root.grid_rowconfigure(0, weight=1)
        self.UI_root.grid_columnconfigure(0, weight=1)
        self.UI_root.minsize(900, 700)
        sc = ScrollableContainer(self.UI_root, bd=2, scroll='vertical')

        self.image_references = []  # keeps references so they don't dissapear
        __list_results = self.user_account.fetch_user_listed_inventory()
        if len(__list_results)!=0:
            __i=0
            for __list_row in __list_results:
                __i+=1
                self.display_list_tool_gui(sc.container, __list_row)    
        else:
            Label(self.UI_root_frame, text='Your inventory is empty', font=("Helvetica", 20)).grid(padx=100, pady=300)
        sc.grid(row=0, column=0, sticky='nsew')
        self.UI_root.mainloop()        

    def display_list_tool_gui(self, __parent, __list_row, **kw):

        __item_info_dict = dict(zip(self.user_account.Inventory_Table_Index, __list_row))
        __Tool_Frame = self.add_label_frame(
            __parent, __item_info_dict.get('Item_Name'), ipadx=50, ipady=30, padx=5, pady=5)

        photo = PhotoImage(file = r".\random.png")
        
        self.image_references.append(photo.subsample(4, 4))
        Label(__Tool_Frame, image=self.image_references[len(self.image_references)-1]).grid(rowspan=4, padx=20, pady=10,)

        _list=[]
        _list.append('Half day rate: ' + self.get_displayable_price(__item_info_dict.get('Half_Day_Fee')))
        _list.append('Full day rate: ' + self.get_displayable_price(__item_info_dict.get('Full_Day_Fee')))
        _list.append('Current process state: ' + __item_info_dict.get('Item_Process_State'))
        _list.append('Item Number: ' + __item_info_dict.get('Unique_Item_Number'))
    
        
        _row_end=1
        _column_offset =1
        _list_len = len(_list)/2 + _column_offset
        _column_start = _column_offset
        _column_end = int(_list_len)

        if _column_end != _list_len:
            case="uneven"
            _column_end += 1
        else:
            case="even"
        def add_Label(__text, _column, _row):
            Label(__Tool_Frame, text=__text).grid(row=_row, column=_column, padx=30, sticky="nw")
        _index=0
        for _i in range(_column_start,_column_end):
            for _j in range(0, _row_end+1):
                if case == "even":
                    add_Label(_list[_index], _i, _j)
                elif case=="uneven":
                    if(_i!=_column_end):
                        add_Label(_list[_index], _i, _j)
                _index+=1


        item_descrition = Text(__Tool_Frame, wrap=WORD, height=3, width=50)
        item_descrition.grid(row=3, column=1, columnspan=100)

        _desc_amalgam = __item_info_dict.get('Description', "error")
        _desc = _desc_amalgam.replace("\\n", " ")
        _max_char_len = 130
        if len(_desc) > _max_char_len:
            _new_desc = ""
            _word_list = _desc.split(" ")
            for _word in _word_list:
                if len(_new_desc) < _max_char_len:
                    _new_desc += f" {_word}"
            _desc = _new_desc + " ( . . . ) "
        # for _i in _desc_list:
        #     _line = _i.strip('\\t')
        item_descrition.insert('end', _desc)
        item_descrition.config(state=DISABLED)
        # take kw
        # labelframe, display Tool Name, half day rate and full day rate and button to bring up a separate individual page
        # change make calendar show events, put dates in an array and save on db
        # for loop to go through all dates?
        # load array from db and and select dates on calendar

        # load photo from db

    def menu_view_current_orders(self):
        pass  # TODO

    def menu_view_purchase_history(self):
        pass  # TODO

    def menu_view_next_invoice(self):
        pass  # TODO

    def view_own_tool_inventory(self):
        pass  # TODO
        # get own tool inventory

    def quit(self):
        self.UI_root.destroy()
        self.UI_root.quit()

    ##### random method for Class functionality #####

    def run_current_menu(self):
        self.current_menu()

    def goto_register_user_menu(self, event):
        self.register_user_ui()

    def get_all_children(self):
        __list = self.UI_root.winfo_children()
        for item in __list:
            if item.winfo_children():
                __list.extend(item.winfo_children())
        return __list

    def get_buffered_user_errors(self):
        __db_class_error_buffer = self.user_account.dbInterface.db_class_error_buffer
        if(len(__db_class_error_buffer)>0):
            self.buffered_user_errors.append(str("#"*40))
            self.buffered_user_errors.append("Database Class Errors:")
            self.buffered_user_errors.extend(__db_class_error_buffer)
        __user_class_error_buffer = self.user_account.user_class_error_buffer
        if(len(__user_class_error_buffer)>0):
            self.buffered_user_errors.append(str("#"*40))
            self.buffered_user_errors.append("User Class Errors:")
            self.buffered_user_errors.extend(__user_class_error_buffer)
        buffered_errors = tuple(self.buffered_user_errors)
        self.buffered_user_errors.clear()
        return buffered_errors

    def get_savable_int_price(self, __price):
        return int(float(price_str(__price))*100)
    
    def get_displayable_price(self, __price):
        return "£ "+str(price_dec(str(float(__price)/100)))


    ########################################################    Main Program    ###########################################


if __name__ == '__main__':
    program = uiInterface()
    # program.run()
    program.log_in_ui(email="test@test", password = "123456789") # Just to TEST
