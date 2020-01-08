import uuid
import datetime
from tkinter import StringVar, PanedWindow, Button
from Classes.tkinterwidgets.getfileswidget import GetImagesWidget
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass


def register_user_UI(self):
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - Register New User")
    self.add_menu_bar_UI_2()
    # Parent
    PWparent = PanedWindow(self.root_frame, orient='horizontal')
    # Define StrVars
    first_name_StrVar = StringVar()
    surname_StrVar = StringVar()
    phone_number_StrVar = StringVar()
    birthday_date_StrVar = StringVar()
    post_code_StrVar = StringVar()
    home_address_StrVar = StringVar()
    town_StrVar = StringVar()
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
        ("Town:", town_StrVar),
        ("Email: ", email_StrVar),
        ("Password: #{type=pw", password_StrVar),
        ("Confirm Password: #{type=pw", confirm_password_StrVar),
        ("User Type: ", None),
        ("User Photo: ", None)
    ])
    # Date Entry
    self.place_date_entry_get_entry(
        PWparent, birthday_date_StrVar, row=3, column=1, columnspan=2, sticky='w')
    # Radio Buttons
    user_type_IntVar = self.place_usertype_entry_get_var(
        PWparent,
        "Tool User",
        "Tool Owner",
        row=10,
        sticky='w'
    )
    # Files Widget
    images_widget = GetImagesWidget(
        PWparent, empty_message='Add Photo', max_items=1)
    images_widget.grid(row=11, column=1, columnspan=2, pady=4, sticky='w')
    # Class Variables:
    Variables_Dict = {
        "First_Name": first_name_StrVar,
        "Surname": surname_StrVar,
        "Phone_Number": phone_number_StrVar,
        "Date_of_Birth": birthday_date_StrVar,
        "Home_Address": home_address_StrVar,
        "Post_Code": post_code_StrVar,
        "Town": town_StrVar,
        "Email_Address": email_StrVar,
        "Password": password_StrVar,
        "Confirm_Password": confirm_password_StrVar,
        "Type_of_User": user_type_IntVar,
        "Images_Widget": images_widget
    }
    # Register Button
    submit_button = Button(
        PWparent,
        text="Register",
        command=lambda: self.process_register_new_user(
            PWparent, **Variables_Dict)
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
    self.R_first_name = str(kw.pop("First_Name").get())
    self.R_surname = str(kw.pop("Surname").get())
    self.R_phone_number = str(kw.pop("Phone_Number").get())
    self.R_birthday_date = str(kw.pop("Date_of_Birth").get())
    self.R_home_address = str(kw.pop("Home_Address").get())
    self.R_town = str(kw.pop("Town").get())
    self.R_post_code = str(kw.pop("Post_Code").get())
    self.R_email = str(kw.pop("Email_Address").get())
    self.R_password = str(kw.pop("Password").get())
    self.R_confirm_password = kw.pop("Confirm_Password").get()
    self.R_type_of_user = int(kw.pop("Type_of_User").get())
    # Clear errors already displayed
    self.clear_errors()
    # Buffer errors if any
    self.validate_register_user_input()
    # Check buffer
    if(len(self.buffered_errors) == 0):
        images_widget = kw.get("Images_Widget")
        reg_U_packed_images_db_list = self.get_image_paths_str_DB_ready(
            images_widget)
        self.user_instance.register(
            Unique_User_ID=str(int(uuid.uuid1())),
            First_Name=self.R_first_name,
            Surname=self.R_surname,
            Date_of_Birth=self.R_birthday_date,
            Phone_Number=self.R_phone_number,
            Home_Address=self.R_home_address,
            Town=self.R_town,
            Post_Code=self.R_post_code,
            Email_Address=self.R_email,
            Password=self.R_password,
            Type_of_User="Tool_User" if self.R_type_of_user == 1 else "Tool_Owner",
            Profile_Photo=reg_U_packed_images_db_list
        )
        self.log_in_UI()
    else:
        self.generate_output_errors_UI(
            _parent, column=3,
            padx=50,  sticky='se'
        )


def validate_register_user_input(self):
    if(self.R_first_name == ""):
        self.buffered_errors.append("Please enter your first name")
    if(self.R_surname == ""):
        self.buffered_errors.append("Please enter your surname")
    if self.user_instance.does_email_exist(self.R_email):
        self.buffered_errors.append("Email already exists")
    if (self.R_email.find("@") == -1):
        self.buffered_errors.append("Please enter a valid email")
    try:
        __numberStr = self.R_phone_number
        if __numberStr == "":
            self.buffered_errors.append("Please enter a phone number")
        self.R_phone_number = int(__numberStr)
    except:
        self.buffered_errors.append("Please enter a valid phone number")
    if self.R_birthday_date == self.datetime_to_string(datetime.datetime.now()):
        self.buffered_errors.append("Please enter a valid date")
    if(self.R_post_code == ""):
        self.buffered_errors.append("Please enter your postcode")
    if(self.R_home_address == ""):
        self.buffered_errors.append("Please enter your home address")
    if not (self.R_password == self.R_confirm_password):
        self.buffered_errors.append("Passwords do not match")
    if not 8 <= len(self.R_password) <= 32:
        self.buffered_errors.append(
            "Please enter a password w/ 8 - 32 digits")
    if (self.R_type_of_user == 0):
        self.buffered_errors.append("Please select the type of account")
