import datetime
import calendar
from tkinter import Label, LabelFrame, Frame, Entry, Text, Button, StringVar, OptionMenu, messagebox, Toplevel
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
    from Classes.tkinterwidgets.getfileswidget import GetImagesWidget, DisplayImagesWidget
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def view_month_invoice_UI(self):
    self.go_back_menu = self.menu_user_options_UI
    self.reset_window()
    self.root.resizable(width=True, height=True)
    self.root.title("Shared Power - View Month Invoice")
    self.add_menu_bar_UI_4()
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.minsize(1250, 700)
    sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
    # Get Results
    User_ID = self.user_instance.get_user_unique_ID()
    orders_list = self.order_instance.fetch_orders_from_user_id(User_ID)
    # get month start and end day
    time_now = datetime.datetime.now()
    month = time_now.month
    year = time_now.year
    x = calendar.monthrange(year, month)
    first_day, last_day = x
    start_date_month = self.string_to_datetime(f'{first_day}/{month}/{year}')
    end_date_month = self.string_to_datetime(f'{last_day}/{month}/{year}')
    __i = 0
    invoiced_orders_list = []
    old_uninvoiced_orders = []
    for order in orders_list:
        __i += 1
        Order_Dictionary = dict(
            zip(self.order_instance.orders_table_Index, order))
        # Order Start Day
        order_start_day = self.string_to_datetime(
            Order_Dictionary.get('Booking_Start_Day'))
        if Order_Dictionary.get('Order_State') == 'Complete'and Order_Dictionary.get('Invoiced') == '':
            if start_date_month < order_start_day < end_date_month:
                invoiced_orders_list.append(order)
                # mark as invoiced
            elif order_start_day < start_date_month:
                old_uninvoiced_orders.append(order)
            # mark as invoiced
            self.order_instance.update_order(
                Unique_Order_ID=Order_Dictionary.get("Unique_Order_ID"),
                Invoiced=f'{month}/{year}'
            )

            # add invoice attribute to orders
    print(invoiced_orders_list)
    print(old_uninvoiced_orders)
    # check if there any invoices from previous months that haven't been invoiced
    # output all to a Text box?
    self.go_back_menu()
    # invoice class to record invoices
