try:  # Otherwise pylint complains
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


class OrderClass:

    def __init__(self, db_link: DatabaseInterfaceClass):
        self.tool_class_error_buffer = []
        self.DB_Link = db_link

        # Create tables if not already created:
        __order_table_column_values_tuple = (
            "Unique_Item_Number", str,
            "Unique_User_ID", str,
            "Unique_Order_ID", str,
            "Order_Date", str,
            "Pick_Up_Fee", str,
            "Drop_Off_Fee", str,
            "Order_Type", str,
            "Order_Hours", str,
            "Availability_Start_Date", str,
            "Availability_End_Date", str,
            "Customer_Feedback", str,
            "Customer_Condition_Photos", str
        )
        self.orders_table = "Orders_Table"
        self.orders_table_Index = self.DB_Link.create_table_from_tuple(
            self.orders_table, __order_table_column_values_tuple)

        # the method "create_table_from_tuple" creates the tables and returns a list of the column values
        # similar to the lists above but without the datatypes in between

    def record_order(self, **kwargv):
        self.DB_Link.select_table(self.orders_table)
        order_details = []
        for i in self.orders_table_Index:
            order_details.append(kwargv.pop(i))
        if len(kwargv) > 1:
            self.tool_class_error_buffer.append(
                "ERROR - Unknown kwards were passed into the record order method")
        else:
            self.DB_Link.data_entry(order_details)

    def update_order(self, **kwargv):
        self.DB_Link.select_table(self.orders_table)
        order_ID = kwargv.pop("Unique_Order_ID", "0")
        indentifying_expr = f"Unique_Order_ID = '{order_ID}'"
        for column_name in kwargv:
            updated_item = kwargv.get(column_name)
            if type(updated_item) == str:
                replace_with_expr = f"{column_name} = '{updated_item}'"
            else:
                replace_with_expr = f"{column_name} = {updated_item}"
            self.DB_Link.update_database(
                indentifying_expr, replace_with_expr
            )

    def cancel_order(self, order_ID="0"):
        self.DB_Link.select_table(self.orders_table)
        indentifying_expr = f"Unique_Item_Number = '{order_ID}'"
        self.DB_Link.delete_line(indentifying_expr)

    def fetch_orders(self, User_ID):
        self.DB_Link.select_table(self.orders_table)
        __list_results = self.DB_Link.fetch_lines_from_db(
            f"Unique_User_ID = '{User_ID}'")
        return __list_results


if __name__ == '__main__':
    print("Please run the program from __init__.py")
