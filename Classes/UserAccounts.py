import enum
import time
import datetime
import uuid
import bcrypt
from abc import ABC, abstractmethod
from enum import Enum, auto

# Local Imports
from Classes.DatabaseInterface import DatabaseInterface


class E_User_Details_Table(enum.Enum):
    # this enum is to be used with: fetched_user_details
    Unique_User_ID = 0
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


User_Details_Table_Index = [
    "Unique_User_ID",
    "First_Name",
    "Surname",
    "Date_of_Birth",
    "Phone_Number",
    "Home_Address",
    "Post_Code",
    "Email_Address",
    "Password_Hash",
    "Outstanding_Balance",
    "Type_of_User",
]


class UserClass():

    def __init__(self):
        self.session_ID = 0
        # Use this to implement a system that uses this ID to redirect
        # the user to the correct menu (Tool Owner vs Tool User)
        # I may save this ID to the database?
        # Encrypt Session?
        self.database_name = "Database"
        self.user_details_table = "User_Details"
        self.orders_table = "Orders"
        self.inventory_table = "Tool_Inventory"
        self.fetched_user_details = []

        # Create tables if not already created:
        self.dbInterface = DatabaseInterface(self.database_name)
        self.dbInterface.create_table(
            self.user_details_table,
            # Remember to update the enum if any of the these values gets changed
            "Unique_User_ID", int,
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
        self.dbInterface.create_table(
            self.orders_table,
            "Order_Date", str,
            "Item_Number", int,
            "Price", int,
            "Pick_Up_Fee", int,
            "Drop_Off_Fee", int,
            "Pick_Up_Date", str,
            "Drop_Off_Date", str,
            "Customer_Feedback", str
        )
        self.dbInterface.create_table(
            self.inventory_table,
            "Item_Number", int,
            "Item_Name", str,
            "Half_Day_Fee", int,
            "Full_Day_Fee", int,
            "Description", str,
            "Availability", str,
            "Item_Process_State", str,
            "User_ID", int
        )

    def register(self, *argv):
        self.dbInterface.select_table(self.user_details_table)
        self.dbInterface.data_entry(argv)

    def register_tool(self, *argv):
        self.dbInterface.select_table(self.inventory_table)
        tool_info_and_owner = list(argv)
        tool_info_and_owner.append("TODO_Item_Process_State")
        tool_info_and_owner.append(
            self.fetched_user_details[User_Details_Table_Index.index("Unique_User_ID")])
        self.dbInterface.data_entry(tuple(tool_info_and_owner))

    def does_email_exist(self, __user_email: str):
        return self.update_fetched_user_details(__user_email)

    def update_fetched_user_details(self, __user_email: str):
        try:
            self.dbInterface.select_table(self.user_details_table)
            __list_line_results = self.dbInterface.fetch_lines_from_database(
                f"Email_Address = '{__user_email}'")
            # Gets the first result, there should only be one
            self.fetched_user_details = __list_line_results[0]
            print(self.fetched_user_details)
            if(len(__list_line_results) > 1):
                print("Database ERROR - There is more than 1 match for the given email")
            return True
        except:
            return False

    def fetch_user_listed_inventory(self):
        self.dbInterface.select_table(self.inventory_table)
        __list_results = self.dbInterface.fetch_lines_from_database(
            f"User_ID = {self.fetched_user_details[User_Details_Table_Index.index('Unique_User_ID')]}")
        return __list_results

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
        __byte_str_password_hash = self.fetched_user_details[E_User_Details_Table.Password_Hash.value].encode(
            "utf-8")
        return True if bcrypt.checkpw(__byte_str_pw, __byte_str_password_hash) else False

    def get_user_type(self):
        return self.fetched_user_details[E_User_Details_Table.Type_of_User.value]

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
