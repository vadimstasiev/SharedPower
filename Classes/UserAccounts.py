import enum
import time
import datetime
import uuid
import bcrypt
from abc import ABC, abstractmethod
from enum import Enum, auto

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface


class User_Details_Table(enum.Enum):
    # this enum is to be used with: fetched_user_details
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


class UserDefault():

    def __init__(self):
        self.database_name = "Database"
        self.user_details_table = "User_Details"
        self.orders_table = "Orders"
        self.fetched_user_details = []

        # The following parameters will be used to create the table column values if it's not already created
        self.dbInterface = DatabaseInterface(
            self.database_name,
            self.user_details_table,
            # Remember to update the enum if any of the these values gets changed
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
        # self.dbInterface.create_table(
        #     self.database_name,
        #     self.orders_table,
        #     "Order_Date", str,
        #     "Item_Number", int,
        #     "Price", int,
        #     "Pick_Up_Fee", int,
        #     "Drop_Off_Fee", int,
        #     "Pick_Up_Date", str,
        #     "Drop_Off_Date", str,
        #     "Customer_    Feedback", str
        # )

    def register(self, *argv: tuple):
        # write stuff to database
        self.dbInterface.data_entry(argv)
        self.fetched_user_details = list(argv)

    def does_email_exist(self, __user_email: str):
        return self.update_fetched_user_details(__user_email)

    def update_fetched_user_details(self, __user_email: str):
        try:
            __all_rows_that_match_the_email = self.dbInterface.fetch_line_from_database(
                f"Email_Address = '{__user_email}'")
            self.fetched_user_details = __all_rows_that_match_the_email[0]
            print(self.fetched_user_details)
            if(len(__all_rows_that_match_the_email) > 1):
                print("Database ERROR - There is more than 1 match for the given email")
            return False
        except:
            return True

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
        __byte_str_password_hash = self.fetched_user_details[User_Details_Table.Password_Hash.value].encode(
            "utf-8")
        return True if bcrypt.checkpw(__byte_str_pw, __byte_str_password_hash) else False

    def get_user_type(self):
        return self.fetched_user_details[User_Details_Table.Type_of_User.value]

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
