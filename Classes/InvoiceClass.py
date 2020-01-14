try:  # Otherwise pylint complains
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


class InvoiceClass:

    def __init__(self, db_link: DatabaseInterfaceClass):
        self.tool_class_error_buffer = []
        self.DB_Link = db_link

        # Create tables if not already created:
        __order_table_column_values_tuple = (
            "Month_Invoice_ID", str,
            "Unique_User_ID", str,
            "Total", str,
        )
        self.invoice_table = "Invoice_Table"
        self.invoice_table_Index = self.DB_Link.create_table_from_tuple(
            self.invoice_table, __order_table_column_values_tuple)

        # the method "create_table_from_tuple" creates the tables and returns a list of the column values
        # similar to the lists above but without the datatypes in between

    def record_invoice(self, **kwargv):
        self.DB_Link.select_table(self.invoice_table)
        invoice_details = []
        for i in self.invoice_table_Index:
            invoice_details.append(kwargv.pop(i, ''))
        if len(kwargv) > 1:
            self.tool_class_error_buffer.append(
                "ERROR - Unknown kwargs were passed into the record invoice method")
        else:
            self.DB_Link.data_entry(invoice_details)

    def update_invoice(self, **kwargv):
        self.DB_Link.select_table(self.invoice_table)
        invoice_ID = kwargv.pop("Month_Invoice_ID", "0")
        indentifying_expr = f"Month_Invoice_ID = '{invoice_ID}'"
        for column_name in kwargv:
            updated_item = kwargv.get(column_name)
            if type(updated_item) == str:
                replace_with_expr = f"{column_name} = '{updated_item}'"
            else:
                replace_with_expr = f"{column_name} = {updated_item}"
            self.DB_Link.update_database(
                indentifying_expr, replace_with_expr
            )

    def fetch_invoice_by_month_id(self, Month_Invoice_ID):
        self.DB_Link.select_table(self.invoice_table)
        __list_results = self.DB_Link.fetch_lines_from_db(
            f"Month_Invoice_ID = '{Month_Invoice_ID}'")
        invoice = {}
        if len(__list_results) > 0:
            invoice = dict(zip(self.invoice_table_Index, __list_results[0]))
        return invoice


if __name__ == '__main__':
    print("Please run the program from __init__.py")
