import enum
import time
import datetime
import uuid
import bcrypt
from abc import ABC, abstractmethod
from enum import auto

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface


class UserType(enum.Enum):
    User_Default = 1
    Tool_Owner = 2


class User_Details_Column_Values(enum.Enum):
    Unique_ID = 0
    First_Name = 1
    Surname = 2
    Date_of_Birth = 3
    Phone_Number = 4
    Home_Address = 5
    Post_Code = 6
    Email_Address = 7
    Password_Hash = 8
    Outstanding_Balance = 9
    Type_of_User = 10


class UserDefault():  # Use this as a container

    def __init__(self):
        # fetch data from database
        # check to see if account is on database
        # if not then ADD it
        self.database_name = "Database"
        self.table_name = "User_Details"
        self.local_user_info_list = []

        # The following parameters will be the table column values if it's not already created
        self.dbInterface = DatabaseInterface(
            self.database_name,
            self.table_name,
            "Unique_ID", int,
            "First_Name", str,
            "Surname", str,
            "Date_of_Birth", str,
            "Phone_Number", int,
            "Home_Address", str,
            "Post_Code", str,
            "Email_Address", str,
            "Password_Hash", str,
            "Outstanding_Balance", int,
            "Type_of_User", str
        )

        # call the distructor if account name or account number is not valid
        # self.__account_number = account_number

    @staticmethod
    def login(self):
        pass

    def register(self, *argv: tuple):
        # write stuff to database
        self.dbInterface.data_entry(argv)
        self.local_user_info_list = list(argv)

    def update_local_user_info_list(self, __user_email: str):
        try:
            __all_rows_that_match_the_email = self.dbInterface.read_from_database(
                f"Email_Address = '{__user_email}'")
            self.local_user_info_list = __all_rows_that_match_the_email[0]
            print(self.local_user_info_list)
            if(len(__all_rows_that_match_the_email) > 1):
                print("ERROR - There is more than 1 match for the given email")
            return False
        except:
            return True

    # def does_user_exist(self, __user_email: str):
    #     return True if self.local_user_info_list[User_Details_Column_Values.Email_Address.value] == __user_email else False

    @staticmethod
    def generate_hashed_password(__password: str):
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_hashed = bcrypt.hashpw(__byte_str_pw, bcrypt.gensalt())
        __hashed = __byte_str_hashed.decode("utf-8")
        return __hashed

    @staticmethod
    def generate_unique_ID():
        __unique_number = int(uuid.uuid1())
        return __unique_number

    def check_password(self, __email: str, __password: str):
        # check if email exists
        # get password hash from database
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_password_hash = self.local_user_info_list[User_Details_Column_Values.Password_Hash.value].encode(
            "utf-8")
        return True if bcrypt.checkpw(__byte_str_pw, __byte_str_password_hash) else False

    def identify_user(self):  # STATIC CLASS
        # fetch from database the user type
        __databaseFetchUserType = "Tool User"
        if (__databaseFetchUserType == "Tool User"):
            pass
        elif (__databaseFetchUserType == "Tool Owner"):
            pass
        else:
            print("Error - Type of User Unknown")
            self.menu_first_access()

    def deliver_to_depot(self, tool):
        # Call the tool as being delivered from the tool class
        pass

    def collect_from_depot(self, tool):
        # Call the tool as being collected from the depot
        pass

    def deliver_to_depotThirdParty(self, tool):
        self.deliver_to_depot(tool)
        # Add fee

    def collect_from_depotThirdParty(self, tool):
        self.collect_from_depot(tool)
        # Add fee

    def get_account_number(self):
        return self.__account_number

    def get_account_name(self):
        return self.__account_name


####This is Useless
# class ToolOwner(UserDefault):
#     def __init__(self, account_name, account_number):
#         UserDefault.__init__(account_name, account_number)
#         self.typeOfAccount = "tool owner"
#         # add more specific stuff to the tool owners
#         pass
