# please install the following non-standard libraries: bcrypt, pillow (should no longer be needed) , tkcalendar (includes Babel which is needed)

import sys
import time
import datetime
import os
import shutil
from tkinter import *
from typing import List

# Import local classes
from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
from Classes.tkinterwidgets.getfileswidget import GetFilesWidget, GetImagesWidget
from Classes.tkinterwidgets.calendar_ import Calendar
from Classes.tkinterwidgets.dateentry import DateEntry
from Classes.MoneyParser import price_str, price_dec
from Classes.DatabaseInterface import DatabaseInterface
from Classes.UserAccount import UserAccount


class UI_Interface:
    def __init__(self):
        self.UI_root = Tk()
        self.buffered_user_errors = []
        self.outputed_errors_list = []
        self.user_account = UserAccount()

    def run(self):
        self.log_in_UI()

    def log_in_UI(self, **kw):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)
        self.UI_root.title("Shared Power - Log in")
        self.add_menu_bar_1()
        # Parent
        PWparent = PanedWindow(self.UI_root_frame, orient=HORIZONTAL)
        PWparent.grid(row=0, column=1, padx=50, pady=20)
        # StrVars
        email_StrVar = StringVar()
        password_StrVar = StringVar()
        # Labels and Entries
        self.generate_UI_label_and_entry(
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
        registerB.bind('<Button-1>', self.goto_register_user_menu)
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
        self.UI_root.bind('<Return>', Return_keypressed)
        # Generate any already existent errors
        self.generate_UI_output_errors(PWparent, starting_index=100)
        # This is usefull for automatic login:
        if len(kw) > 0:
            email_StrVar.set(kw.get('email', ''))
            password_StrVar.set(kw.get('password', ''))
            self.process_log_in()
        self.UI_root.mainloop()

    def process_log_in(self, **kw):
        email, password = self.email.get(), self.password.get()
        self.clear_errors()
        if not (self.user_account.does_email_exist(email)):
            self.buffered_user_errors.append("Account not found")
        else:
            if(self.user_account.check_password(email, password)):
                __account_user_type = self.user_account.get_user_type()
                self.menu_user_options_UI()
            else:
                self.buffered_user_errors.append("Wrong Password")
        self.generate_UI_output_errors(self.UI_root_frame, starting_index=100)

    def register_user_UI(self):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)
        self.UI_root.title("Shared Power - Register New User")
        self.add_menu_bar_2()
        # Parent
        PWparent = PanedWindow(self.UI_root_frame, orient=HORIZONTAL)
        # Define StrVars
        first_name_StrVar = StringVar()
        surname_StrVar = StringVar()
        phone_number_StrVar = StringVar()
        birthday_date_StrVar = StringVar()
        post_code_StrVar = StringVar()
        home_address_StrVar = StringVar()
        email_StrVar = StringVar()
        password_StrVar = StringVar()
        confirm_password_StrVar = StringVar()
        # Labels and Entries
        self.generate_UI_label_and_entry(PWparent, [  # None = do not generate Entry, useful for different input widgets
            ("First Name: ", first_name_StrVar),
            ("Surname: ", surname_StrVar),
            ("Phone Number: ", phone_number_StrVar),
            ("Date of Birth: ", None),
            ("Post Code: ", post_code_StrVar),
            ("Home Address:", home_address_StrVar),
            ("Email: ", email_StrVar),
            ("Password: #{type=pw", password_StrVar),
            ("Confirm Password: #{type=pw", confirm_password_StrVar),
            ("User Type: ", None),
            ("User Photo: ", None)
        ])
        # Date Entry
        self.add_date_entry(PWparent, birthday_date_StrVar, row=3, column=1, columnspan=2, sticky=W)
        # Radio Buttons
        user_type_IntVar = self.add_two_radio_buttons_get_var(
            PWparent,
            "Tool User",
            "Tool Owner",
            row=9,
            sticky=W
        )
        # Files Widget
        self.files_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=1)
        self.files_widget.grid(row=10, column=1, columnspan=2, pady=4, sticky=W)
        # Class Variables:
        Variables_Dict = {
            "First_Name":first_name_StrVar,
            "Surname":surname_StrVar,
            "Phone_Number":phone_number_StrVar, 
            "Date_of_Birth":birthday_date_StrVar,
            "Home_Address":home_address_StrVar, 
            "Post_Code":post_code_StrVar, 
            "Email_Address": email_StrVar, 
            "Password": password_StrVar, 
            "Confirm_Password": confirm_password_StrVar, 
            "Type_of_User": user_type_IntVar
        }
        # Register Button
        submit_button = Button(PWparent, text="Register", command=lambda: self.process_register_new_user(**Variables_Dict))
        submit_button.grid(column=2, ipadx=10, ipady=5)
        # Bind return key to proceed
        def Return_keypressed(event):
            self.process_register_new_user(**Variables_Dict)
        self.UI_root.bind('<Return>', Return_keypressed)
        ###########
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.UI_root.mainloop()

    def process_register_new_user(self, **kw):
        self.reg_U_first_name = str(kw.pop("First_Name").get())
        self.reg_U_surname = str(kw.pop("Surname").get())
        self.reg_U_phone_number = str(kw.pop("Phone_Number").get())
        self.reg_U_birthday_date = str(kw.pop("Date_of_Birth").get())
        self.reg_U_home_address = str(kw.pop("Home_Address").get())
        self.reg_U_post_code = str(kw.pop("Post_Code").get())
        self.reg_U_email = str(kw.pop("Email_Address").get())
        self.reg_U_password = str(kw.pop("Password").get())
        self.reg_U_confirm_password = kw.pop("Confirm_Password").get()
        self.reg_U_type_of_user = int(kw.pop("Type_of_User").get())

        self.clear_errors() # clear errors already displayed
        self.validate_register_user_input() # buffers errors if any
        if(len(self.buffered_user_errors) == 0): # checks buffer
            reg_U_packed_images_db_list = self.get_images_from_widget(self.files_widget)
            self.user_account.register(
                first_name=self.reg_U_first_name,
                surname=self.reg_U_surname,
                bithday=self.reg_U_birthday_date,
                phone_number=self.reg_U_phone_number,
                home_address=self.reg_U_home_address,
                post_code=self.reg_U_post_code,
                email=self.reg_U_email,
                password=self.reg_U_password,
                user_type="Tool_User" if self.reg_U_type_of_user == 1 else "Tool_Owner",
                profile_photo=reg_U_packed_images_db_list
            )
            self.log_in_UI()
        else:
            self.generate_UI_output_errors(
                PWparent, column=3, padx=50,  sticky=SE)

    def validate_register_user_input(self):
        if(self.reg_U_first_name == ""):
            self.buffered_user_errors.append("Please enter your first name")
        if(self.reg_U_surname == ""):
            self.buffered_user_errors.append("Please enter your surname")
        if self.user_account.does_email_exist(self.reg_U_email):
            self.buffered_user_errors.append("Email already exists")
        if (self.reg_U_email.find("@") == -1):
            self.buffered_user_errors.append("Please enter a valid email")
        try:
            __numberStr = self.reg_U_phone_number
            if __numberStr == "":
                self.buffered_user_errors.append("Please enter a phone number")
            self.reg_U_phone_number = int(__numberStr)
        except:
            self.buffered_user_errors.append("Please enter a valid phone number")
        if self.reg_U_birthday_date == self.datetime_to_string(datetime.datetime.now()):
            self.buffered_user_errors.append("Please enter a valid date")
        if(self.reg_U_post_code == ""):
            self.buffered_user_errors.append("Please enter your postcode")
        if(self.reg_U_home_address == ""):
            self.buffered_user_errors.append("Please enter your home address")
        if not (self.reg_U_password == self.reg_U_confirm_password):
            self.buffered_user_errors.append("Passwords do not match")
        if not 8 <= len(self.reg_U_password) <= 32:
            self.buffered_user_errors.append("Please enter a password w/ 8 - 32 digits")
        if (self.reg_U_type_of_user == 0):
            self.buffered_user_errors.append("Please select the type of account")

    def register_tool_UI(self):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)
        self.UI_root.title("Shared Power - Register New Tool")
        self.add_menu_bar_4()
        PWparent = LabelFrame(self.UI_root_frame, text="Register Tool")
        # Labels and entries
        self.tool_name = StringVar()
        self.half_day_rate = StringVar()
        self.full_day_rate = StringVar()
        self.generate_UI_label_and_entry(PWparent, [  # None = do not generate Entry, useful for different input widgets
            ("Tool Name: ", self.tool_name),
            ("Description: ", None),
            ("Half day rate: ", self.half_day_rate),
            ("Full Day Rate: ", self.full_day_rate),
            ("Availablity start date: ", None),
            ("Availablity end date: ", None),
            ("Choose Photo: ", None),
        ])
        self.description_text_box = Text(
            PWparent, wrap=WORD, height=10, width=80)
        self.description_text_box.grid(row=1, column=1, columnspan=5)
        # Start date Widget
        self.availability_start_date_StrVar = StringVar()
        self.add_date_entry(
            PWparent, self.availability_start_date_StrVar, row=4, column=1, columnspan=2, sticky=W)
        # End date Widget
        self.availability_end_date_StrVar = StringVar()
        self.add_date_entry(
            PWparent, self.availability_end_date_StrVar, row=5, column=1, columnspan=2, sticky=W)
        # Get Photo Widget
        self.files_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=5)
        self.files_widget.grid(row=6, column=1, columnspan=2, sticky=W)
        # Register Button
        __registerB = Button(PWparent, text="Register", command=self.process_register_or_update_tool)
        __registerB.grid(column=5, ipadx=10, ipady=5)    
        
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.go_back_menu = self.menu_user_options_UI
        self.UI_root.mainloop()

    def process_register_or_update_tool(self):  # TODO TODO TODO
        self.validate_register_tool_input()
        reg_T_availability_list = [
            str(self.availability_start_date_StrVar.get()),
            str(self.availability_end_date_StrVar.get())
        ]
        if(len(self.buffered_user_errors) == 0):
            self.clear_errors()
            reg_T_packed_images_db_list = self.get_images_from_widget(self.files_widget)
            self.user_account.register_tool(
                item_name=self.reg_T_tool_name,
                half_day_fee=self.get_savable_int_price(self.reg_T_half_day_rate),
                full_day_fee=self.get_savable_int_price(self.reg_T_full_day_rate),
                description=self.reg_T_description,
                availability=self.pack_availability_dates_DB_READY(reg_T_availability_list),
                photos=reg_T_packed_images_db_list
            )
            self.go_back_menu()
        else:
            self.clear_errors()
            self.generate_UI_output_errors(
                PWparent, column=0, starting_index=100, padx=50,  sticky=SE)

    def validate_register_tool_input(self):
        self.reg_T_tool_name = str(self.tool_name.get())
        self.reg_T_description = str(self.description_text_box.get("1.0", 'end-1c'))
        self.reg_T_half_day_rate = str(self.half_day_rate.get())
        self.reg_T_full_day_rate = str(self.full_day_rate.get())

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
            price_dec(self.reg_T_half_day_rate)
        except:
            self.buffered_user_errors.append(
                "Please enter a valid price for the half day rate")

        if self.reg_T_full_day_rate == 0:
            self.buffered_user_errors.append(
                "Please enter the full day rate")
        try:
            price_dec(self.reg_T_full_day_rate)
        except:
            self.buffered_user_errors.append(
                "Please enter a valid price for the full day rate")
        # if self.reg_T_availability_start_date == datetime.datetime.now().strftime('%d/%m/%Y'):
        #     self.buffered_user_errors.append(
        #         "Please Enter a Valid Date")

    def pack_availability_dates_DB_READY(self, reg_T_availability_list):
        __list = reg_T_availability_list
        __reg_T_availability_str_pack = __list[0]
        for __date in __list:
            __reg_T_availability_str_pack += '#' + __date
        return __reg_T_availability_str_pack

    def pair_dates_from_DB_packed(self, __DB_packed_dates):
        __list = __DB_packed_dates.split('#')
        unpacked_dates=[]
        for i in __list:
            unpacked_dates.append(i.strip('#'))
        pair_list = []
        for i in range(0, len(unpacked_dates)-1, 2):
            start_date = unpacked_dates[i]
            end_date = unpacked_dates[i+1]
            pair_list.append((self.string_to_datetime(start_date), self.string_to_datetime(end_date)))
        return pair_list


    def generate_UI_label_and_entry(self, __widget, __list, **kw):
        __label_padx = kw.pop('label_width', 20)
        __entry_width = kw.pop('entry_width', 25)

        str_keywords = [
            "{type=pw",
        ]
        label_list = []
        entries_list = []
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
            label_list.append(__label)
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
                entries_list.append(__entry)
            else:
                entries_list.append(None)
        return label_list, entries_list
            

    def generate_UI_output_errors(self, __widget, **kw):
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

    def generate_UI_functions_menu(self, __widget, __list, **kw):
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
        de_kw = {}
        _date = kw.pop("date", "default")
        if _date != "default":
            de_kw["day"]=_date.day
            de_kw["month"]=_date.month
            de_kw["year"]=_date.year
        _mindate = kw.pop("mindate", "")
        _maxdate = kw.pop("maxdate", "")
        if _mindate != "" and _maxdate!="":
            de_kw["mindate"]=_mindate
            de_kw["maxdate"]=_max
        __date_entry = DateEntry(__widget, width=22, textvariable=__var, date_pattern='d/m/yyyy', **de_kw)
        __date_entry.grid(kw)
        return __date_entry

    def add_label_frame(self, __widget, __text, **kw):
        __label_frame = LabelFrame(__widget, text=__text)
        __label_frame.grid(kw)
        return __label_frame

    def add_two_radio_buttons_get_var(self, __widget, __textB1, __textB2, **kw):
        __user_type_input = IntVar()
        __radio_button1 = Radiobutton(__widget, text="Tool User", variable=__user_type_input,
                                      value=1)
        __radio_button2 = Radiobutton(__widget, text="Tool Owner", variable=__user_type_input,
                                      value=2)
        kw['column'] = 1
        __radio_button1.grid(kw)
        kw['column'] = 2
        __radio_button2.grid(kw)
        return __user_type_input

    def clear_errors(self):
        for __l in self.outputed_errors_list:
            __l.destroy()


    def menu_user_options_UI(self):
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)


        self.add_menu_bar_3()

        __account_user_type = self.user_account.get_user_type()
        button_text_and_functions = []
        if (__account_user_type == "Tool_User"):
            button_text_and_functions = [
                ("Search for tools", None),
                ("View current orders", None),
                ("View next Invoice", None),
                ("Log Out", self.log_in_UI),
            ]
        elif (__account_user_type == "Tool_Owner"):
            button_text_and_functions = [
                ("Register tool", self.register_tool_UI),
                ("View Listed Inventory", self.menu_listed_inventory_UI),
                ("Search for tools", None),
                ("View current orders", None),
                ("View Purchase History", None),
                ("View next Invoice", None),
                ("Log Out", self.log_in_UI),
            ]
        else:
            self.buffered_user_errors.append("Database Error - Type of User Unknown")  
            self.log_in_UI()
        self.generate_UI_functions_menu(self.UI_root_frame, button_text_and_functions)

        
        returned_images = self.get_db_images(self.user_account.fetched_user_dictionary, 'Profile_Photo', 4)
        if len(returned_images)>0:
            photo_frame = Frame(self.UI_root)
            user_photo = Label(photo_frame, text='User Photo', image=returned_images[0]).grid(padx=40, row=0)
            user_name = self.user_account.fetched_user_dictionary.get('First_Name')
            user_name += " " + self.user_account.fetched_user_dictionary.get('Surname')
            Label(photo_frame, text=user_name, font=("Helvetica", 13)).grid(padx=40, sticky='n',row =1)
            photo_frame.grid(column=2, pady=40, row=0, sticky='n')


        self.UI_root.mainloop()

    def get_db_images(self, _fetched_dictionary: dict, _dict_element: str, _subsample=4):
        list_unpacked_images_path = self.unpack_db_images_path(_fetched_dictionary.get(_dict_element, ""))
        photo_image_object_list = []
        for _image_path in list_unpacked_images_path:
            try:
                photo_image_object_list.append(PhotoImage(file=_image_path.strip('#{@!#')).subsample(_subsample))
            except:
                pass # image doesn't exist
        self.image_references.extend(photo_image_object_list)
        return photo_image_object_list

    def unpack_db_images_path(self, packed_images_path: str):
        list_unpacked_images_path = []
        if packed_images_path !='':
            list_packed_images_path = packed_images_path.split('#{@!#')
            for _image_path in list_packed_images_path:
                try:
                    list_unpacked_images_path.append(_image_path.strip('#{@!#'))
                except:
                    pass # image doesn't exist
        return list_unpacked_images_path

    def setup_new_window(self):
        self.UI_root.title("Shared Power")
        self.UI_root.resizable(width=True, height=True)
        self.UI_root.minsize(0, 0)
        self.UI_root.unbind('<Return>')
        __list = self.get_all_children()
        for __child in __list:
            __child.destroy()
        self.UI_root_frame = Frame(self.UI_root, height=2, bd=1)
        self.UI_root.geometry("")
        self.UI_root_frame.grid()
        self.image_references = []  # keeps references so they don't dissapear


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
        __submenu.add_command(label="Go Back", command=self.log_in_UI)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)

    def add_menu_bar_3(self):   # used for the tool users/owners UI
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Log Out", command=self.log_in_UI)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)

    def add_menu_bar_4(self):   # used for the sub pages of the tool users/owners UI
        __user_type = self.user_account.get_user_type()
        self.menubar = Menu(self.UI_root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=lambda: self.go_back_menu())
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.UI_root.config(menu=self.menubar)



    def menu_listed_inventory_UI(self):  # TODO
        self.go_back_menu = self.menu_user_options_UI
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=True)
        self.UI_root.title("Shared Power - View Stock Inventory")
        self.add_menu_bar_4()
        self.UI_root.grid_rowconfigure(0, weight=1)
        self.UI_root.grid_columnconfigure(0, weight=1)
        self.UI_root.minsize(900, 700)
        sc = ScrollableContainer(self.UI_root, bd=2, scroll='vertical')

        __list_results = self.user_account.fetch_user_listed_inventory()
        if len(__list_results)!=0:
            __i=0
            for __list_row in __list_results:
                __i+=1
                self.display_list_tool_UI(sc.container, __list_row)    
        else:
            Label(self.UI_root_frame, text='Your inventory is empty', font=("Helvetica", 20)).grid(padx=100, pady=300)
        sc.grid(row=0, column=0, sticky='nsew')
        self.UI_root.mainloop()        

    def display_list_tool_UI(self, __parent, __list_row, **kw):
        # create item dictionary
        item_dictionary = dict(zip(self.user_account.Inventory_Table_Index, __list_row))
        # create parent
        PWparent = LabelFrame(
            __parent,
            text=item_dictionary.get('Item_Name')
        )
        images_path_list = self.unpack_db_images_path(item_dictionary.get('Tool_Photos', ''))
        returned_images = self.get_db_images(item_dictionary, 'Tool_Photos', 4)
        # Place photo if one exists
        if len(returned_images)>0: 
            Label(PWparent, image=returned_images[0]).grid(rowspan=4, padx=20, pady=10)
        # Labels to display
        _list=[
            'Half day rate: ' + self.get_displayable_price(item_dictionary.get('Half_Day_Fee')),
            'Full day rate: ' + self.get_displayable_price(item_dictionary.get('Full_Day_Fee')),
            'Current process state: ' + item_dictionary.get('Item_Process_State'),
            'Item Number: ' + item_dictionary.get('Unique_Item_Number')
        ]
        # Display labels in a 2 row x X column configuration
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
            Label(PWparent, text=__text).grid(row=_row, column=_column, padx=30, sticky="nw")
        _index=0
        for _i in range(_column_start,_column_end):
            for _j in range(0, _row_end+1):
                if case == "even":
                    add_Label(_list[_index], _i, _j)
                elif case=="uneven":
                    if(_i!=_column_end):
                        add_Label(_list[_index], _i, _j)
                _index+=1
        # Place item description
        item_descrition = Text(PWparent, wrap=WORD, height=3, width=50)
        item_descrition.grid(row=3, column=1, columnspan=100)
        # Get item description and trim it to fit the box 
        _desc_amalgam = item_dictionary.get('Description', "error")
        _desc = _desc_amalgam.replace("\\n", " ")
        _max_char_len = 130
        if len(_desc) > _max_char_len:
            _new_desc = ""
            _word_list = _desc.split(" ")
            for _word in _word_list:
                if len(_new_desc) < _max_char_len:
                    _new_desc += f" {_word}"
            _desc = _new_desc + " ( . . . ) "
        # Output item description
        item_descrition.insert('end', _desc)
        item_descrition.config(state=DISABLED)
        # View/Edit item button
        viewB = Button(PWparent,
            text="Edit",
            command=lambda: self.edit_individual_tool_UI(item_dictionary, images_path_list))
        viewB.grid(column=3, columnspan=2,pady=10, ipadx=40, ipady=2)
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)

    def edit_individual_tool_UI(self, tool_information_dict, images_path_list): # TODO refactor
        self.go_back_menu = self.menu_listed_inventory_UI
        self.setup_new_window()
        self.UI_root.resizable(width=False, height=False)
        self.UI_root.title("Shared Power - Edit Tool")
        self.add_menu_bar_4()
        
        # create parent
        LBtext = "Edit Tool: " + tool_information_dict.get("Item_Name")
        PWparent = LabelFrame(
            self.UI_root_frame,
            text=LBtext
        )

        self.tool_name = StringVar()
        self.half_day_rate = StringVar()
        self.full_day_rate = StringVar()
        self.post_code_StrVar = StringVar()
        self.availability_start_date_StrVar = StringVar()
        self.availability_end_date_StrVar = StringVar()

        label_text_and_vars = [  # None = do not generate Entry, useful for different input widgets
            ("Tool Name:", self.tool_name),             #0
            ("Description:", None),                     #1
            ("Half day rate:", self.half_day_rate),     #2
            ("Full Day Rate:", self.full_day_rate),     #3
            ("Availability start date:", None),         #4
            ("Availablity end date:", None),            #5
            ("Dates Booked:", None),                    #6
            ("Choose Photo:", None),                    #7

        ]
        label_list, entries_list = self.generate_UI_label_and_entry(
            PWparent, label_text_and_vars)
        # Fill the empty entries 
        entries_list[0].insert(0,tool_information_dict.get("Item_Name"))
        entries_list[2].insert(0,self.get_displayable_price(tool_information_dict.get("Half_Day_Fee")))
        entries_list[3].insert(0,self.get_displayable_price(tool_information_dict.get("Full_Day_Fee")))
        # description textbox
        item_description = Text(PWparent, wrap=WORD, height=10, width=80)
        item_description.grid(row=1, column=1, columnspan=5)
        _desc = tool_information_dict.get('Description', "error").replace('\\n', ' \n')
        item_description.insert('end', _desc)
        # Get Availability List
        Availability_Pair_List = self.pair_dates_from_DB_packed(tool_information_dict.get("Availability", ''))
        # Date entry start date
        availability_start_date= Availability_Pair_List[0][0]
        self.availability_start_date_str = StringVar()
        start_dateentry = self.add_date_entry(
            PWparent, self.availability_start_date_str, row=4, column=1, columnspan=2, sticky=W, date=availability_start_date)
        if availability_start_date<datetime.datetime.now(): 
            start_dateentry.config(state=DISABLED)
            Label(PWparent, text="Not editable if tool was already available").grid(row=4, column=3, sticky=W)

        # Date entry end date
        availability_end_date= Availability_Pair_List[len(Availability_Pair_List)-1][1]
        self.availability_end_date_str = StringVar()
        end_dateentry = self.add_date_entry(
            PWparent, self.availability_end_date_str, row=5, column=1, columnspan=2, sticky=W, date=availability_end_date)
        if len(Availability_Pair_List)>1:
            end_dateentry.config(state=DISABLED)
            Label(PWparent, text="Not editable if tool was already booked").grid(row=5, column=3, sticky=W)
            

        # View bookings
        Button(PWparent, text='View Bookings',command=lambda: self.view_bookings_UI(Availability_Pair_List)).grid(row=6, column=1, columnspan=2, sticky=W)

        # Custom GetImagesWidget
        self.files_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=5)
        self.files_widget.grid(row=7, column=1, columnspan=2, sticky=W)
        self.files_widget.automatic__file_input(images_path_list)


        # Buttons
        Button(PWparent, text="Update Tool Information", command=self.process_register_or_update_tool).grid(
            column=5, ipadx=10, ipady=5, sticky='e')
        Button(PWparent, text="Remove Tool Listing", command=self.process_register_or_update_tool).grid(
            column=5, ipadx=10, ipady=5, sticky='e') 
        


        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.UI_root.mainloop()
        # must check for the difference in images added in the actual process

    def view_bookings_UI(self, availability_Pair_dict):
            booked_dates = list(tuple(availability_Pair_dict))
            startday, endday = booked_dates.pop(0)
            top = Toplevel(self.UI_root)
            cal = Calendar(top, selectmode='none', date_pattern='d/m/yyyy', day=startday.day, month=startday.month, year=startday.year)
            # mindate and maxdate from Calendar are broken, DO NOT USE
            for dates in booked_dates:
                start_date, end_date = dates
                for i in range(0, (end_date-start_date).days+1):
                    date = start_date + cal.timedelta(days=i)
                    cal.calevent_create(date, 'Booked', 'booked')
            cal.tag_config('booked', background='red', foreground='yellow')
            cal.pack(fill="both", expand=True)
    
    #### TODO MENUS
    def menu_search_for_tools(self):
        pass  # TODO
    
    def menu_view_current_orders(self):
        pass  # TODO

    def menu_view_purchase_history(self):
        pass  # TODO

    def menu_view_next_invoice(self):
        pass  # TODO


    ##### random method for Class functionality #####

    def goto_register_user_menu(self, event):
        self.register_user_UI()

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

    def get_images_from_widget(self, __wgt):
        images_path_list = __wgt.get_PATHS()
        images_db_list = ''
        if not os.path.exists('Images'):
            os.makedirs('Images')
        for i in images_path_list:
            destination = './Images/' + str(self.user_account.generate_unique_ID())
            __extension = ''
            for j in range(i.rindex('.'), len(i)):
                    __extension += i[j]
            destination+=__extension
            shutil.copyfile(i, destination)
            images_db_list+=destination + '#{@!#'
        return images_db_list # returns a single string with all paths, ready to be saved on a DB

    def get_savable_int_price(self, __price):
        return int(float(price_str(__price))*100)
    
    def get_displayable_price(self, __price):
        return "£ "+str(price_dec(str(float(__price)/100)))

    def datetime_to_string(self, _datetime: datetime.datetime):
        return _datetime.strftime('%d/%m/%Y')

    def string_to_datetime(self, _string: str):
        return datetime.datetime.strptime(_string, '%d/%m/%Y')

    def contact_admin(self):
        print("Contact Admin")
        # IDK what to do here, do something fancy lol
        # Can add message inbox to admin's personal db for that stuff, logs, etc
        # Can also create an interface for an admin account

    def quit(self):
        self.UI_root.destroy()
        self.UI_root.quit()

    ########################################################    Main Program    ###########################################


if __name__ == '__main__':
    program = UI_Interface()
    # program.run()
    program.log_in_UI(email="test@test", password = "123456789") # Just to TEST
