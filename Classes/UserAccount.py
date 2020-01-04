import enum
import time
import datetime
import uuid
import bcrypt
from tkinter import Image  # for the image type

#from abc import ABC, abstractmethod

# Local Imports
try:
    from Classes.DatabaseInterface import DatabaseInterface
except:
    pass


class UserAccount():

    def __init__(self):
        self.user_class_error_buffer = []
        self.database_name = "Database"
        self.dbInterface = DatabaseInterface(self.database_name)
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
            "Outstanding_Balance", int,
            "Type_of_User", str,
            "Profile_Photo", str
        )
        self.user_details_table = "User_Details"
        self.User_Details_Table_Index = self.dbInterface.create_table_from_tuple(
            self.user_details_table, __user_details_column_values_tuple)

        __orders_table_column_values_tuple = (
            "Order_Date", str,
            "Item_Number", int,
            "Price", int,
            "Pick_Up_Fee", int,
            "Drop_Off_Fee", int,
            "Pick_Up_Date", str,
            "Drop_Off_Date", str,
            "Customer_Feedback", str
        )
        self.orders_table = "Orders"
        self.Orders_Table_Index = self.dbInterface.create_table_from_tuple(
            self.orders_table, __orders_table_column_values_tuple)

        __inv_table_column_values_tuple = (
            "Unique_Item_Number", str,
            "Item_Name", str,
            "Half_Day_Fee", int,
            "Full_Day_Fee", int,
            "Description", str,
            "Availability", str,
            "Item_Process_State", str,
            "User_ID", int,
            "Tool_Photos", str
        )
        self.inventory_table = "Tool_Inventory"
        self.Inventory_Table_Index = self.dbInterface.create_table_from_tuple(
            self.inventory_table, __inv_table_column_values_tuple)

        self.fetched_user_dictionary = {}
        # the method "create_table_from_tuple" creates the tables and returns a list of the column values
        # similar to the lists above but without the datatypes in between

    def register(self, **kw):
        self.dbInterface.select_table(self.user_details_table)
        __password_hash = self.generate_hashed_password(
            kw.pop("password", "None"))
        user_details = (
            str(self.generate_unique_ID()),
            kw.pop("first_name", "None"),
            kw.pop("surname", "None"),
            kw.pop("birthday", "00/00/00"),
            kw.pop("phone_number", 0),
            kw.pop("home_address", "None"),
            kw.pop("post_code", "None"),
            kw.pop("email", "None"),
            __password_hash,
            kw.pop("outstanding_balance", 0),
            kw.pop("user_type", "Tool_Owner"),
            kw.pop("profile_photo", ""),
        )
        if len(kw) > 1:
            self.user_class_error_buffer(
                "ERROR - Please Update the user register method to match the given kw")
        self.dbInterface.data_entry(user_details)

    def register_tool(self, **kw):
        self.dbInterface.select_table(self.inventory_table)
        tool_info = (
            str(self.generate_unique_ID()),
            kw.pop("item_name", "None"),
            kw.pop("half_day_fee", 0),
            kw.pop("full_day_fee", 0),
            kw.pop("description", "None"),
            kw.pop("availability", ""),
            kw.pop("item_process_state", "Error"),
            self.fetched_user_dictionary.get('Unique_User_ID'),
            kw.pop("photos", "")
        )
        if len(kw) > 1:
            self.user_class_error_buffer(
                "ERROR - Please Update the tool register method to match the given kw")
        self.dbInterface.data_entry(tool_info)

    def update_tool(self, **kw):
        tool_ID = kw.pop("tool_ID", "0")
        self.dbInterface.select_table(self.inventory_table)
        tool_info = (
            tool_ID,
            kw.pop("item_name", "None"),
            kw.pop("half_day_fee", 0),
            kw.pop("full_day_fee", 0),
            kw.pop("description", "None"),
            kw.pop("availability", "None"),
            kw.pop("item_process_state", "Error"),
            self.fetched_user_dictionary.get('Unique_User_ID'),
            kw.pop("photos", "")
        )
        if len(kw) > 1:
            self.user_class_error_buffer(
                "ERROR - Please Update the tool updater method to match the given kw")
        _updated_tool_dict = zip(self.Inventory_Table_Index, tool_info)
        indentifying_expr = f"Unique_Item_Number = '{tool_ID}'"
        for element in _updated_tool_dict:
            column_name, updated_item = element
            replace_with_expr = f"{column_name} = '{updated_item}'"
            self.dbInterface.update_database(
                indentifying_expr, replace_with_expr)

    def delete_tool(self, tool_ID="0"):
        self.dbInterface.select_table(self.inventory_table)
        indentifying_expr = f"Unique_Item_Number = '{tool_ID}'"
        self.dbInterface.delete_line(indentifying_expr)

    def does_email_exist(self, __user_email: str):
        return self.update_fetched_user_details(__user_email)

    def update_fetched_user_details(self, __user_email: str):
        user_details_updated_b = False
        try:
            self.dbInterface.select_table(self.user_details_table)
            __list_line_results = self.dbInterface.fetch_lines_from_db(
                f"Email_Address = '{__user_email}'")
            # Gets the first result, there should only be one
            __fetched_user_details = __list_line_results[0]
            self.fetched_user_dictionary = dict(
                zip(self.User_Details_Table_Index, __fetched_user_details))
            # print(self.fetched_user_dictionary)
            user_details_updated_b = True
            if(len(__list_line_results) > 1):
                self.dbInterface.db_class_error_buffer.append(
                    "Database ERROR - There is more than 1 match for the given email")
                user_details_updated_b = False
        except:
            pass
        return user_details_updated_b

    def fetch_user_listed_inventory(self):
        self.dbInterface.select_table(self.inventory_table)
        __user_unique_id = self.fetched_user_dictionary.get('Unique_User_ID')
        __list_results = self.dbInterface.fetch_lines_from_db(
            f"User_ID = {__user_unique_id}")  # This is for an SQL query, returns list with all the inventory of a given user
        return __list_results

    def generate_hashed_password(self, __password: str):
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_hashed = bcrypt.hashpw(__byte_str_pw, bcrypt.gensalt())
        __hashed = __byte_str_hashed.decode("utf-8")
        return __hashed

    def generate_unique_ID(self):
        __unique_number = int(uuid.uuid1())
        return __unique_number

    def check_password(self, __email: str, __password: str):
        __byte_str_pw = __password.encode("utf-8")
        __byte_str_password_hash = self.fetched_user_dictionary.get(
            'Password_Hash').encode("utf-8")
        return True if bcrypt.checkpw(__byte_str_pw, __byte_str_password_hash) else False

    def get_user_type(self):
        return self.fetched_user_dictionary.get('Type_of_User')

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


if __name__ == '__main__':
    print("Please run the program from __init__.py")
