import uuid
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass


class ToolClass:

    def __init__(self, db_link: DatabaseInterfaceClass):
        self.tool_class_error_buffer = []
        self.DB_Link = db_link

        # Create tables if not already created:

        __inv_table_column_values_tuple = (
            "Unique_Item_Number", str,
            "Unique_User_ID", str,
            "Item_Name", str,
            "Half_Day_Fee", int,
            "Full_Day_Fee", int,
            "Description", str,
            "Availability_Start_Date", str,
            "Availability_End_Date", str,
            "Item_Process_State", str,
            "Tool_Photos", str
        )
        self.inventory_table = "Tool_Inventory"
        self.Inventory_Table_Index = self.DB_Link.create_table_from_tuple(
            self.inventory_table, __inv_table_column_values_tuple)

        # the method "create_table_from_tuple" creates the tables and returns a list of the column values
        # similar to the lists above but without the datatypes in between

    def register_tool(self, **kwargv):
        self.DB_Link.select_table(self.inventory_table)
        tool_details = []
        for i in self.Inventory_Table_Index:
            tool_details.append(kwargv.pop(i))
        if len(kwargv) > 1:
            self.tool_class_error_buffer.append(
                "ERROR - Please Update the tool register method to match the given kwargv")
        else:
            self.DB_Link.data_entry(tool_details)

    def update_tool(self, **kw):
        tool_ID = kw.pop("tool_ID", "0")
        self.DB_Link.select_table(self.inventory_table)
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
            self.tool_class_error_buffer.append(
                "ERROR - Please Update the tool updater method to match the given kw")
        _updated_tool_dict = zip(self.Inventory_Table_Index, tool_info)
        indentifying_expr = f"Unique_Item_Number = '{tool_ID}'"
        for element in _updated_tool_dict:
            column_name, updated_item = element
            replace_with_expr = f"{column_name} = '{updated_item}'"
            self.DB_Link.update_database(
                indentifying_expr, replace_with_expr)

    def delete_tool(self, tool_ID="0"):
        self.DB_Link.select_table(self.inventory_table)
        indentifying_expr = f"Unique_Item_Number = '{tool_ID}'"
        self.DB_Link.delete_line(indentifying_expr)

    def fetch_user_listed_inventory(self, user_unique_id):
        #user_unique_id = self.fetched_user_dictionary.get('Unique_User_ID')
        self.DB_Link.select_table(self.inventory_table)
        __list_results = self.DB_Link.fetch_lines_from_db(
            f"Unique_User_ID = '{user_unique_id}'")  # Returns list with all the inventory of a given user
        return __list_results


if __name__ == '__main__':
    print("Please run the program from __init__.py")
