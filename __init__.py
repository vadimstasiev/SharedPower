# please install the following non-standard libraries: bcrypt, pillow (should no longer be needed) , tkcalendar (includes Babel which is needed)

import sys
import time
import datetime
import os
import shutil
from tkinter import *
from tkinter import messagebox
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
        self.root = Tk()
        self.buffered_user_errors = []
        self.outputed_errors_list = []
        self.user_account = UserAccount()

    def run(self):
        self.log_in_UI()

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
        if not (self.user_account.does_email_exist(email)):
            self.buffered_user_errors.append("Account not found")
        else:
            if(self.user_account.check_password(email, password)):
                self.menu_user_options_UI()
            else:
                self.buffered_user_errors.append("Wrong Password")
        self.generate_output_errors_UI(self.root_frame, starting_index=100)

    def register_user_UI(self):
        self.reset_window()
        self.root.resizable(width=False, height=False)
        self.root.title("Shared Power - Register New User")
        self.add_menu_bar_UI_2()
        # Parent
        PWparent = PanedWindow(self.root_frame, orient=HORIZONTAL)
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
        self.generate_labels_and_entries_UI(PWparent, [  # None = do not generate Entry
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
        self.place_date_entry_get_entry(PWparent, birthday_date_StrVar, row=3, column=1, columnspan=2, sticky=W)
        # Radio Buttons
        user_type_IntVar = self.place_usertype_entry_get_var(
            PWparent,
            "Tool User",
            "Tool Owner",
            row=9,
            sticky=W
        )
        # Files Widget
        images_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=1)
        images_widget.grid(row=10, column=1, columnspan=2, pady=4, sticky=W)
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
            "Type_of_User": user_type_IntVar,
            "Images_Widget":images_widget
        }
        # Register Button
        submit_button = Button(
            PWparent,
            text="Register",
            command=lambda: self.process_register_new_user(PWparent, **Variables_Dict)
        )
        submit_button.grid(column=2, ipadx=10, ipady=5)
        # Bind return key to proceed
        def Return_keypressed(event):
            self.process_register_new_user(PWparent, **Variables_Dict)
        self.root.bind('<Return>', Return_keypressed)
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.root.mainloop()

    def process_register_new_user(self, _parent, **kw):
        # Define class variables that hold information in a relevant format
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
        # Clear errors already displayed
        self.clear_errors()
        # Buffer errors if any
        self.validate_register_user_input() 
        # Check buffer
        if(len(self.buffered_user_errors) == 0): 
            images_widget = kw.get("Images_Widget")
            reg_U_packed_images_db_list = self.get_image_paths_str_DB_ready(images_widget)
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
            self.generate_output_errors_UI(
                _parent, column=3,
                padx=50,  sticky=SE
            )

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
        self.reset_window()
        self.root.resizable(width=False, height=False)
        self.root.title("Shared Power - Register New Tool")
        self.add_menu_bar_UI_4()
        PWparent = LabelFrame(self.root_frame, text="Register Tool")
        # StrVars
        toolname_StrVar = StringVar()
        half_rate_StrVar = StringVar()
        full_rate_StrVar = StringVar()
        # Labels and entries
        self.generate_labels_and_entries_UI(PWparent, [
            ("Tool Name:", toolname_StrVar),
            ("Description:", None),
            ("Half day rate:", half_rate_StrVar),
            ("Full Day Rate:", full_rate_StrVar),
            ("Availablity start date:", None),
            ("Availablity end date:", None),
            ("Choose Photo:", None),
        ])
        # Description Box
        description_box = Text(
            PWparent,
            wrap=WORD,
            height=10,
            width=80
        )
        description_box.grid(row=1, column=1, columnspan=5)
        # Start date Widget
        start_date_StrVar = StringVar()
        self.place_date_entry_get_entry(
            PWparent, start_date_StrVar, row=4, column=1, columnspan=2, sticky=W)
        # End date Widget
        end_date_StrVar = StringVar()
        self.place_date_entry_get_entry(
            PWparent, end_date_StrVar, row=5, column=1, columnspan=2, sticky=W)
        # Get Photo Widget
        images_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=3)
        images_widget.grid(row=6, column=1, columnspan=2, sticky=W)
        # Variable Dictionary
        VariableDict= { 
            "Tool_Name":toolname_StrVar,
            "Description_Box":description_box,
            "Half_Day_Rate":half_rate_StrVar,
            "Full_Day_Rate":full_rate_StrVar,
            "Start_Date":start_date_StrVar,
            "End_Date":end_date_StrVar,
            "Images_Widget":images_widget
        }
        # Register Button
        registerB = Button(
            PWparent,
            text="Register",
            command=lambda:self.process_register_or_update_tool(PWparent, **VariableDict)
        )
        registerB.grid(column=5, ipadx=10, ipady=5)    
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.go_back_menu = self.menu_user_options_UI
        self.root.mainloop()

    def process_register_or_update_tool(self, _parent, **kw):  # TODO TODO TODO
        # Class Vars, they are public so they can be validated
        reg_T_tool_ID = kw.pop("Tool_ID", "0")
        self.reg_T_tool_name = str(kw.pop("Tool_Name").get())
        self.reg_T_description = str(kw.pop("Description_Box").get("1.0", 'end-1c')).replace("'","''")
        self.reg_T_half_day_rate = str(kw.pop("Half_Day_Rate").get())
        self.reg_T_full_day_rate = str(kw.pop("Full_Day_Rate").get())
        process_state = kw.pop("Process_State", StringVar()).get()
        if process_state!="":
            self.reg_T_process_state = str(process_state)
        else:
            self.reg_T_process_state = "with owner"

        _dates_list = (
            self.string_to_datetime(kw.pop("Start_Date").get()),
            self.string_to_datetime(kw.pop("End_Date").get())
        )
        _existent_list_pair = kw.pop("Original_Availability_Pair_List", [_dates_list])
        _existent_list_pair[0] = _dates_list
        reg_T_availability_list = self.pack_availability_dates_DB_READY(_existent_list_pair)
        images_widget = kw.get("Images_Widget")
        Update = kw.pop("Update", False)
        # Validate Vars
        self.validate_register_tool_input()
        # Check if Vars produced any errors
        if(len(self.buffered_user_errors) == 0):
            self.clear_errors()

            reg_T_packed_images_db_list = self.get_image_paths_str_DB_ready(images_widget)
            kwargs = {
                'tool_ID':reg_T_tool_ID,
                'item_name':self.reg_T_tool_name,
                'half_day_fee':self.get_savable_int_price(self.reg_T_half_day_rate),
                'full_day_fee':self.get_savable_int_price(self.reg_T_full_day_rate),
                'description':self.reg_T_description,
                'availability':reg_T_availability_list,
                'item_process_state':self.reg_T_process_state,
                'photos':reg_T_packed_images_db_list
            }
            if Update:
                self.user_account.update_tool(**kwargs)
            else:
                self.user_account.register_tool(**kwargs)
            self.go_back_menu()
        else:
            self.clear_errors()
            self.generate_output_errors_UI(_parent,
                column=0, starting_index=100,
                padx=50, sticky=SE
            )

    def validate_register_tool_input(self):
        if(self.reg_T_tool_name == ""):
            self.buffered_user_errors.append(
                "Please enter the tool name")
        if(self.reg_T_description == ""):
            self.buffered_user_errors.append(
                "Please enter a description")
        if self.reg_T_half_day_rate == 0:
            self.buffered_user_errors.append(
                "Please enter the half day rate")
        try:
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

    def delete_tool(self, tool_ID, images_to_delete):
        answer = messagebox.askyesnocancel(
            "Delete Tool Listing",
            "Are you sure that you want to remove this listing?",
            icon = 'warning'
        )
        if answer == YES:
            self.user_account.delete_tool(tool_ID)
            self.delete_images(images_to_delete)
            self.go_back_menu()

    def delete_images(self, image_path_list):
        for image in image_path_list:
            os.remove(image)

    def pack_availability_dates_DB_READY(self, availability_list_pair):
        pair_list = availability_list_pair
        packed_availability_str = ""
        for pair in pair_list:
            for date in pair:
                packed_availability_str += '#' + self.datetime_to_string(date)
        packed_availability_str = packed_availability_str.replace("#","",1) # Remove first "#"
        return packed_availability_str

    def unpack_dates_from_DB(self, __DB_packed_dates):
        __list = __DB_packed_dates.split('#')
        unpacked_dates=[]
        for i in __list:
            unpacked_dates.append(i.strip('#'))
        pair_list = []
        for i in range(0, len(unpacked_dates)-1, 2):
            start_date = unpacked_dates[i]
            end_date = unpacked_dates[i+1]
            pair_list.append((self.string_to_datetime(start_date), self.string_to_datetime(end_date)))
        return pair_list    # Returns a list with the dates paired e.g. [[start_date][end_date],[start_date][end_date], etc]

    def generate_labels_and_entries_UI(self, __widget, __list, **kw):
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

    def generate_output_errors_UI(self, __widget, **kw):
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

    def generate_action_buttons_UI(self, __widget, __list, **kw):
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

    def place_date_entry_get_entry(self, __widget, __var, **kw):
        de_kw = {}
        _date = kw.pop("date", "default")
        if _date != "default":
            de_kw["day"]=_date.day
            de_kw["month"]=_date.month
            de_kw["year"]=_date.year
        __date_entry = DateEntry(__widget, width=22, textvariable=__var, date_pattern='d/m/yyyy', **de_kw)
        __date_entry.grid(kw)
        return __date_entry

    def place_usertype_entry_get_var(self, __widget, __textB1, __textB2, **kw):
        __user_type_input = IntVar()
        __radio_button1 = Radiobutton(__widget, text="Tool User", variable=__user_type_input,value=1)
        __radio_button2 = Radiobutton(__widget, text="Tool Owner", variable=__user_type_input,value=2)
        kw['column'] = 1
        __radio_button1.grid(kw)
        kw['column'] = 2
        __radio_button2.grid(kw)
        return __user_type_input

    def clear_errors(self):
        for __l in self.outputed_errors_list:
            __l.destroy()

    def menu_user_options_UI(self):
        self.reset_window()
        self.root.resizable(width=False, height=False)
        self.add_menu_bar_UI_3()
        # Get user profile dictionary
        user_profile_dict = self.user_account.fetched_user_dictionary
        # Get user type
        user_type = self.user_account.get_user_type()
        button_text_and_functions = []
        if (user_type == "Tool_User"):
            button_text_and_functions = [
                ("Search for tools", None),
                ("View current orders", None),
                ("View next Invoice", None),
                ("Log Out", self.log_in_UI),
            ]
        elif (user_type == "Tool_Owner"):
            button_text_and_functions = [
                ("Register tool", self.register_tool_UI),
                ("View Listed Inventory", self.view_listed_inventory_UI),
                ("Search for tools", None),
                ("View current orders", None),
                ("View Purchase History", None),
                ("View next Invoice", None),
                ("Log Out", self.log_in_UI),
            ]
        else:
            self.buffered_user_errors.append("Database Error - Type of User Unknown")  
            self.log_in_UI()
        self.generate_action_buttons_UI(self.root_frame, button_text_and_functions)
        # Get list of images for the user profile, there should only be 1
        photoimage_list = self.generate_PhotoImage_list(user_profile_dict.get('Profile_Photo'), 4)
        if len(photoimage_list)>0:
            photo_frame = Frame(self.root)
            # Use the first image on the list
            user_photo = Label(photo_frame, text='User Photo', image=photoimage_list[0]).grid(padx=40, row=0)
            user_name = user_profile_dict.get('First_Name')
            user_name += " " + user_profile_dict.get('Surname')
            Label(photo_frame, text=user_name, font=("Helvetica", 13)).grid(padx=40, sticky='n',row =1)
            photo_frame.grid(column=2, pady=40, row=0, sticky='n')
        self.root.mainloop()

    def generate_PhotoImage_list(self, list_packed_images_path: str, _subsample=4):
        list_unpacked_images_path = self.unpack_db_images_path(list_packed_images_path)
        photo_image_object_list = []
        for _image_path in list_unpacked_images_path:
            try:
                photo_image_object_list.append(PhotoImage(file=_image_path).subsample(_subsample))
            except:
                pass # image doesn't exist
        self.image_references.extend(photo_image_object_list)
        return photo_image_object_list # PhotoImage object list

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

    def reset_window(self):
        self.root.title("Shared Power")
        self.root.resizable(width=True, height=True)
        self.root.minsize(0, 0)
        self.root.unbind('<Return>')
        __list = self.get_all_children()
        for __child in __list:
            __child.destroy()
        self.root_frame = Frame(self.root, height=2, bd=1)
        self.root.geometry("")
        self.root_frame.grid()
        self.image_references = []  # keeps references so they don't dissapear

    def view_listed_inventory_UI(self):
        self.go_back_menu = self.menu_user_options_UI
        self.reset_window()
        self.root.resizable(width=True, height=True)
        self.root.title("Shared Power - View Stock Inventory")
        self.add_menu_bar_UI_4()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.minsize(900, 700)
        sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
        # Get Results
        results_list = self.user_account.fetch_user_listed_inventory()
        # Loop through all results and display them
        if len(results_list)!=0:
            __i=0
            for result_item in results_list:
                __i+=1
                self.display_list_tool_UI(sc.container, result_item)    
        else:
            Label(sc.container, text='Your inventory is empty', font=("Helvetica", 20)).grid(padx=100, pady=300)
        sc.grid(row=0, column=0, sticky='nsew')
        # Show any errors that might have come up 
        self.generate_output_errors_UI(sc.container, padx=50, starting_index=500)
        self.root.mainloop()        

    def display_list_tool_UI(self, __parent, result_item, **kw):
        # create item dictionary
        item_dictionary = dict(zip(self.user_account.Inventory_Table_Index, result_item))
        # create parent
        PWparent = LabelFrame(__parent, text=item_dictionary.get('Item_Name'))
        # Get Image list
        returned_images = self.generate_PhotoImage_list(item_dictionary.get('Tool_Photos'), 4)
        # Place photo if one exists
        if len(returned_images)>0: 
            # Display first image
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
        _desc = _desc_amalgam.replace("\\n", " ").replace("\\t", "").replace("''", "'")
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
            command=lambda: self.edit_individual_tool_UI(item_dictionary))
        viewB.grid(column=3, columnspan=2,pady=10, ipadx=40, ipady=2)
        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)

    def edit_individual_tool_UI(self, tool_information_dict): # TODO refactor
        images_path_list = self.unpack_db_images_path(tool_information_dict.get('Tool_Photos', ''))
        self.go_back_menu = self.view_listed_inventory_UI
        self.reset_window()
        self.root.resizable(width=False, height=False)
        self.root.title("Shared Power - Edit Tool")
        self.add_menu_bar_UI_4()   
        # create parent
        LBtext = "Edit Tool: " + tool_information_dict.get("Item_Name")
        PWparent = LabelFrame(
            self.root_frame,
            text=LBtext
        )
        # StrVars
        toolname_StrVar = StringVar()
        half_rate_StrVar = StringVar()
        full_rate_StrVar = StringVar()
        start_date_StrVar = StringVar()
        end_date_StrVar = StringVar()
        process_state_StrVar = StringVar()
        # Generate Labels and Entries
        label_list, entries_list = self.generate_labels_and_entries_UI(PWparent, [
            ("Tool Name:", toolname_StrVar),            #0
            ("Description:", None),                     #1
            ("Half day rate:", half_rate_StrVar),       #2
            ("Full Day Rate:", full_rate_StrVar),       #3
            ("Availability start date:", None),         #4
            ("Availablity end date:", None),            #5
            ("Dates Booked:", None),                    #6
            ("Item Process State:", None),              #7
            ("Choose Photo:", None),                    #8
        ])
        # Fill the empty Entries
        entries_list[0].insert(0,tool_information_dict.get("Item_Name"))
        entries_list[2].insert(0,self.get_displayable_price(tool_information_dict.get("Half_Day_Fee")))
        entries_list[3].insert(0,self.get_displayable_price(tool_information_dict.get("Full_Day_Fee")))
        # Description Textbox
        description_box = Text(PWparent, wrap=WORD, height=10, width=80)
        description_box.grid(row=1, column=1, columnspan=5)
        _desc = tool_information_dict.get('Description', "error").replace('\\n', ' \n').replace("''","'")
        description_box.insert('end', _desc)
        # Get Availability List
        Availability_Pair_List = self.unpack_dates_from_DB(tool_information_dict.get("Availability", ''))
        # Date entry start date
        start_datetime = Availability_Pair_List[0][0]
        start_dateentry = self.place_date_entry_get_entry(
            PWparent,
            start_date_StrVar,
            row=4, column=1,
            columnspan=2, sticky=W,
            date=start_datetime
        )
        if start_datetime<datetime.datetime.now():
            start_dateentry.config(state=DISABLED)
            _message = Label(PWparent, text="Not editable if tool was once already available")
            _message.grid(row=4, column=3, sticky=W)
        # Date entry end date
        end_datetime= Availability_Pair_List[len(Availability_Pair_List)-1][1]
        end_dateentry = self.place_date_entry_get_entry(
            PWparent,
            end_date_StrVar,
            row=5, column=1,
            columnspan=2, sticky=W,
            date=end_datetime
        )
        if len(Availability_Pair_List)>1:
            end_dateentry.config(state=DISABLED)
            _message = Label(PWparent, text="Not editable if tool was once already booked")
            _message.grid(row=5, column=3, sticky=W)  
        # View bookings
        _viewbookingsB = Button(
            PWparent,
            text='View Bookings',
            command=lambda: self.view_bookings_Calendar_UI(Availability_Pair_List)
        )
        _viewbookingsB.grid(row=6, column=1, columnspan=2, sticky=W)
        # Dropdown select
        choices = { 'with owner','with depot','with user','with insurance','being processed'}
        default_selection = tool_information_dict.get('Item_Process_State', 'Error')
        process_state_StrVar.set(default_selection)
        dropdown_select = OptionMenu(PWparent, process_state_StrVar, *choices)
        dropdown_select.grid(row=7, column=1, columnspan=2, sticky=W, pady=5)
        # Custom GetImagesWidget
        images_widget = GetImagesWidget(PWparent, empty_message='Add Photo', max_items=3)
        images_widget.grid(row=8, column=1, columnspan=2, sticky=W)
        images_widget.automatic__file_input(images_path_list)
        # Get Tool ID number
        tool_ID = tool_information_dict.get("Unique_Item_Number")
        # Var Dictionary# need to add item process_State
        VariableDict= { 
            "Tool_ID":tool_ID,
            "Tool_Name":toolname_StrVar,
            "Description_Box":description_box,
            "Half_Day_Rate":half_rate_StrVar,
            "Full_Day_Rate":full_rate_StrVar,
            "Start_Date":start_date_StrVar,
            "End_Date":end_date_StrVar,
            "Images_Widget":images_widget,
            "Process_State":process_state_StrVar,
            "Original_Availability_Pair_List": Availability_Pair_List,
            "Update":True
        }
        # Buttons
        _updateinfoB = Button(
            PWparent,
            text="Update Tool Information",
            command=lambda:self.process_register_or_update_tool(PWparent, **VariableDict)
        )
        _updateinfoB.grid(column=5, ipadx=10, ipady=5, sticky='e')
        _removelisting = Button(
            PWparent, 
            text="Remove Tool Listing",
            command=lambda:self.delete_tool(tool_ID, images_path_list),
        )
        _removelisting.grid(column=5, ipadx=10, ipady=5, sticky='e') 

        PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
        self.root.mainloop()
        # must check for the difference in images added in the actual process

    def view_bookings_Calendar_UI(self, availability_Pair_dict):
            booked_dates = list(tuple(availability_Pair_dict))
            startday, endday = booked_dates.pop(0)
            top = Toplevel(self.root)
            cal = Calendar(top, selectmode='none', date_pattern='d/m/yyyy', day=startday.day, month=startday.month, year=startday.year)
            # mindate and maxdate from Calendar are broken, DO NOT USE
            for dates in booked_dates:
                start_date, end_date = dates
                for i in range(0, (end_date-start_date).days+1):
                    date = start_date + cal.timedelta(days=i)
                    cal.calevent_create(date, 'Booked', 'booked')
            cal.tag_config('booked', background='red', foreground='yellow')
            cal.pack(fill="both", expand=True)

    def add_menu_bar_UI_1(self):   # used for Login Screen
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Contact Admin",
                              command=self.contact_admin)
        self.menubar.add_cascade(label="Forgot Password", menu=__submenu)
        self.menubar.add_command(label="Quit", command=self.quit)
        self.root.config(menu=self.menubar)

    def add_menu_bar_UI_2(self):   # used for Register Screen
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=self.log_in_UI)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.root.config(menu=self.menubar)

    def add_menu_bar_UI_3(self):   # used for the tool users/owners UI
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Log Out", command=self.log_in_UI)
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.root.config(menu=self.menubar)

    def add_menu_bar_UI_4(self):   # used for the sub pages of the tool users/owners UI
        __user_type = self.user_account.get_user_type()
        self.menubar = Menu(self.root)
        __submenu = Menu(self.menubar, tearoff=0)
        __submenu.add_command(label="Go Back", command=lambda: self.go_back_menu())
        __submenu.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=__submenu)
        self.root.config(menu=self.menubar)

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
        __list = self.root.winfo_children()
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

    def get_image_paths_str_DB_ready(self, __wgt: GetImagesWidget):
        images_path_list = __wgt.get_PATHS()
        removed_list, added_list = __wgt.get_difference()
        images_db_list = ''
        if not os.path.exists('Images'):
            os.makedirs('Images')
        for image in images_path_list:
            if image in added_list:
                destination = './Images/' + str(self.user_account.generate_unique_ID())
                __extension = ''
                for j in range(image.rindex('.'), len(image)):
                        __extension += image[j]
                destination+=__extension
                shutil.copyfile(image, destination)
            else:
                destination = image
            images_db_list+=destination + '#{@!#'
        # try to delete unused images
        try:
            self.delete_images(removed_list)
        except:
            pass
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
        self.root.destroy()
        self.root.quit()

    ########################################################    Main Program    ###########################################


if __name__ == '__main__':
    program = UI_Interface()
    # program.run()
    program.log_in_UI(email="test@test", password = "123456789") # Just to TEST
