import bcrypt
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass


class UserClass:

    def __init__(self, db_link: DatabaseInterfaceClass):
        self.user_class_error_buffer = []
        self.user_class_error_buffer = []
        self.DB_Link = db_link

        # Create tables if not already created:
        __user_details_column_values_tuple = (
            "Unique_User_ID", str,
            "First_Name", str,
            "Surname", str,
            "Date_of_Birth", str,
            "Phone_Number", int,
            "Home_Address", str,
            "Post_Code", str,
            "Email_Address", str,
            "Password_Hash", str,
            "Balance", int,
            "Type_of_User", str,
            "Profile_Photo", str
        )
        self.user_details_table = "User_Details"
        self.User_Details_Table_Index = self.DB_Link.create_table_from_tuple(
            self.user_details_table, __user_details_column_values_tuple)

        self.User_Dictionary = {}
        # the method "create_table_from_tuple" creates the tables and returns a list of the column values
        # similar to the lists above but without the datatypes in between

    def register_tool(self, **kwargv):
        self.DB_Link.select_table(self.user_details_table)
        user_details = []
        hashed_password = self.generate_hashed_password(kwargv.pop('Password'))
        kwargv['Password_Hash'] = hashed_password
        kwargv['Balance'] = 0
        for i in self.User_Details_Table_Index:
            user_details.append(kwargv.pop(i))
        if len(kwargv) > 1:
            self.user_class_error_buffer.append(
                "ERROR - Please Update the user register method to match the given kwargv")
        else:
            self.DB_Link.data_entry(user_details)

    def update_User_Dictionary(self, __user_email: str):
        _User_Dict_Was_Updated = False
        try:
            self.DB_Link.select_table(self.user_details_table)
            __list_line_results = self.DB_Link.fetch_lines_from_db(
                f"Email_Address = '{__user_email}'")
            # Gets the first result, there should only be one
            __fetched_user_details = __list_line_results[0]
            self.User_Dictionary = dict(
                zip(self.User_Details_Table_Index, __fetched_user_details))
            # print(self.User_Dictionary)
            _User_Dict_Was_Updated = True
            if(len(__list_line_results) > 1):
                self.DB_Link.db_class_error_buffer.append(
                    "Database ERROR - There is more than 1 match for the given email")
        except:
            pass
        return _User_Dict_Was_Updated

    def check_password(self, __email: str, __password: str):
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_password_hash = self.User_Dictionary.get(
            'Password_Hash').encode("utf-8")
        return True if bcrypt.checkpw(__byte_str_pw, __byte_str_password_hash) else False

    def generate_hashed_password(self, __password: str):
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_hashed = bcrypt.hashpw(__byte_str_pw, bcrypt.gensalt())
        __hashed = __byte_str_hashed.decode("utf-8")
        return __hashed

    def does_email_exist(self, __user_email: str):
        return self.update_User_Dictionary(__user_email)

    # Getters

    def get_user_unique_ID(self):
        return self.User_Dictionary.get('Unique_User_ID')

    def get_user_firstname(self):
        return self.User_Dictionary.get('First_Name')

    def get_user_surname(self):
        return self.User_Dictionary.get('Surname')

    def get_user_birthday(self):
        return self.User_Dictionary.get('Date_of_Birth')

    def get_user_phonenumber(self):
        return self.User_Dictionary.get('Phone_Number')

    def get_user_homeaddress(self):
        return self.User_Dictionary.get('Home_Address')

    def get_user_postcode(self):
        return self.User_Dictionary.get('Post_Code')

    def get_user_email(self):
        return self.User_Dictionary.get('Email_Address')

    def get_user_balance(self):
        return self.User_Dictionary.get('Balance')

    def get_user_type(self):
        return self.User_Dictionary.get('Type_of_User')

    def get_user_profilephotos(self):
        return self.User_Dictionary.get('Profile_Photo')


if __name__ == '__main__':
    print("Please run the program from __init__.py")
