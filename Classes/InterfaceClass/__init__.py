# please install the following non-standard libraries: bcrypt, pillow (should no longer be needed) , tkcalendar (includes Babel which is needed)
from tkinter import Tk
from tkinter import messagebox

# Import local classes
try:  # Otherwise pylint complains
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
    from Classes.UserClass import UserClass
    from Classes.ToolClass import ToolClass
    from Classes.OrderClass import OrderClass
    from Classes.InvoiceClass import InvoiceClass
except:
    pass


class UI_Interface:
    def __init__(self):
        self.root = Tk()
        self.db_link = DatabaseInterfaceClass("Database")
        self.user_instance = UserClass(self.db_link)
        self.tool_instance = ToolClass(self.db_link)
        self.order_instance = OrderClass(self.db_link)
        self.invoice_instance = InvoiceClass(self.db_link)
        self.buffered_errors = []
        self.outputed_errors_list = []
        self.image_references = []
        self.go_back_menu = self.log_in_UI

    def run(self):
        self.log_in_UI()

    from ._login import log_in_UI, process_log_in
    from ._register_user import register_user_UI, process_register_new_user, validate_register_user_input
    from ._register_tool import register_tool_UI, process_register_or_update_tool, validate_register_tool_input
    from ._ui_management import (
        reset_window,
        get_all_children,
        generate_action_buttons_UI,
        generate_labels_and_entries_UI,
        place_date_entry_get_entry,
        place_usertype_entry_get_var,
        add_menu_bar_UI_1,
        add_menu_bar_UI_2,
        add_menu_bar_UI_3,
        add_menu_bar_UI_4,
        contact_admin,
        quit
    )
    from ._user_menu import menu_user_options_UI
    from ._view_edit_inventory import view_listed_inventory_UI, display_list_tool_UI, owner_edit_view_individual_tool_UI, delete_tool
    from ._view_edit_orders import view_listed_orders_UI, display_order_UI, return_or_arrange_collection, mark_as_received, mark_as_returned_to_owner, cancel_order
    from ._view_next_invoice import view_month_invoice_UI, generate_top_invoice_part, generate_line_labels, display_order_line_UI, record_invoice_and_invoiced_orders
    from ._book_tools import user_view_all_tools_UI, user_display_list_tool_UI, display_horizontal_labels, user_view_tool_UI, process_book_tool, validate_booking
    from ._image_related_functions import generate_PhotoImage_list, unpack_db_images_path, delete_images, get_image_paths_str_DB_ready
    from ._date_related_functions import view_bookings_Calendar_UI
    from ._type_conversion import get_savable_int_price, get_displayable_price, datetime_to_string, string_to_datetime
    from ._error_display import get_buffered_user_errors, generate_output_errors_UI, clear_errors


if __name__ == '__main__':
    print("Please run the program from __init__.py")
