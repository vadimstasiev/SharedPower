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
    #####
    FLAT_CHARGE = 500  # Pennies
    ######
    self.go_back_menu = self.menu_user_options_UI
    self.reset_window()
    self.root.resizable(width=True, height=True)
    self.root.title("Shared Power - View Month Invoice")
    self.add_menu_bar_UI_4()
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.minsize(1250, 700)
    sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
    # Parent
    PWparent = LabelFrame(sc.container, text='Invoice')
    PWparent.grid()
    # Get month int and year int
    time_now = datetime.datetime.now()
    month = time_now.month  # int
    year = time_now.year  # int
    ### Get current month ##
    x = calendar.monthrange(year, month)
    first_day, last_day = x
    start_date_month = self.string_to_datetime(
        f'{first_day}/{month}/{year}')  # first day of Current month
    end_date_month = self.string_to_datetime(
        f'{last_day}/{month}/{year}')  # last day of Current month
    # Get User ID
    User_ID = self.user_instance.get_user_unique_ID()
    ### ORDER LISTS ###
    # must make this more efficient
    invoiced_orders_list = self.order_instance.fetch_invoiced_orders(User_ID)  # Gets Invoiced Orders #
    orders_list = self.order_instance.fetch_orders_from_user_id(
        User_ID)  # Get all orders
    __i = 0

    # check if invoice EXISTS
    invoice = self.invoice_instance.fetch_invoice_by_month_id_and_user(
        f'{month}/{year}',
        User_ID
    )
    # create invoice dictionary that either holds all of the invoice values or
    # if they don't exist the keywords will simply not contain anything
    Invoice_Dictionary = dict(
        zip(self.invoice_instance.invoice_table_Index, invoice))
    if len(invoice) > 0:
        pass
    else:
        Invoice_Dictionary['Month_Invoice_ID'] = f'{month}/{year}'
        Invoice_Dictionary['Unique_User_ID'] = User_ID
    self.generate_top_invoice_part(PWparent, Invoice_Dictionary)
    orders_to_set_as_invoiced = []
    total_topay = 0
    for order in orders_list:
        __i += 1
        # Get Dictionaries
        Order_Dictionary = dict(
            zip(self.order_instance.orders_table_Index, order))
        Tool_Dictionary = self.tool_instance.fetch_tool_by_tool_id(
            Order_Dictionary.get('Unique_Item_Number'))
        # Order dates (datetime)
        order_start_day = self.string_to_datetime(
            Order_Dictionary.get('Booking_Start_Day'))
        order_end_day = self.string_to_datetime(
            Order_Dictionary.get('Booking_End_Day'))

        # if Order_Dictionary.get('Invoiced') == '' and Order_Dictionary.get('Order_State') == 'Complete':
        if order_start_day <= end_date_month:
            if Order_Dictionary.get('Order_State') == 'Complete':
                orders_to_set_as_invoiced.append(order)
                # Days Late
                days_late = int(Order_Dictionary.get('Days_Late')) if Order_Dictionary.get(
                    'Days_Late') != '' else 0
                # Day Rates
                half_day_rate = int(Tool_Dictionary.get(
                    'Half_Day_Fee')) if Tool_Dictionary.get('Half_Day_Fee') != '' else 0
                full_day_rate = int(Tool_Dictionary.get(
                    'Full_Day_Fee')) if Tool_Dictionary.get('Full_Day_Fee') != '' else 0
                # Get any applied transportation fees
                pick_up_fee = int(Order_Dictionary.get('Pick_Up_Fee')) if Order_Dictionary.get(
                    'Pick_Up_Fee') != '' else 0
                drop_off_fee = int(Order_Dictionary.get(
                    'Drop_Off_Fee')) if Order_Dictionary.get('Drop_Off_Fee') != '' else 0
                shipping_fees = pick_up_fee+drop_off_fee
                order_total = 0
                # IF ORDER TYPES & Calculate ToTals
                if Order_Dictionary.get('Order_Type') == 'Full Day':
                    order_days = (order_end_day-order_start_day).days
                    late_fees = (days_late*full_day_rate*2)
                    order_total += ((order_days * full_day_rate) +
                                    late_fees + FLAT_CHARGE + shipping_fees)
                if Order_Dictionary.get('Order_Type') == 'Half Day':
                    late_fees = (days_late*full_day_rate*2)
                    order_total += ((1 * half_day_rate) +
                                    late_fees + FLAT_CHARGE + shipping_fees)
                list_of_labels = [
                    Order_Dictionary.get('Order_Date'),
                    Order_Dictionary.get('Unique_Order_ID'),
                    Tool_Dictionary.get('Item_Name'),
                    self.get_displayable_price(late_fees),
                    self.get_displayable_price(shipping_fees),
                    self.get_displayable_price(order_total)
                ]
                if order not in invoiced_orders_list:
                    total_topay += order_total
                    list_of_labels.append('No') # Payed?
                else:
                    list_of_labels.append('Yes') # Payed?
                self.generate_line_labels(
                    PWparent, list_of_labels, __i+6)
    list_of_labels = [
        '', '', '', '', 'INVOICE TOTAL:',
        self.get_displayable_price(total_topay)
    ]
    Invoice_Dictionary['Total'] = total_topay
    self.generate_line_labels(
        PWparent, list_of_labels, __i+7)
    mark_as_payed_B=Button(PWparent, text='Mark as Payed',
           command=lambda: self.record_invoice_and_invoiced_orders(Invoice_Dictionary, orders_to_set_as_invoiced))
    mark_as_payed_B.grid(column=6, row=100, ipadx=30, ipady=10)
           # for order in orders_to_set_as_invoiced, invoice order
    # check if there any invoices from previous months that haven't been invoiced
    # output all to a Text box?
    # invoice class to record invoices
    sc.grid(row=0, column=0, sticky='nsew')
    # Show any errors that might have come up
    self.generate_output_errors_UI(sc.container, padx=50, starting_index=500)
    self.root.mainloop()

def record_invoice_and_invoiced_orders(self, Invoice_Dictionary, Orders_list):
    for order in Orders_list:
        Order_Dictionary = dict(
            zip(self.order_instance.orders_table_Index, order))
        #set order as invoiced
        self.order_instance.update_order(
            Unique_Order_ID=Order_Dictionary.get("Unique_Order_ID"),
            Invoiced=Invoice_Dictionary.get('Month_Invoice_ID')
        )
    self.invoice_instance.record_invoice(**Invoice_Dictionary)
    self.view_month_invoice_UI()

def generate_top_invoice_part(self, parent, Invoice_Dictionary):
    # Invoice ID
    invoice_ID = Invoice_Dictionary.get('Month_Invoice_ID')
    # USER DICTIONARY
    User_Dictionary = self.user_instance.User_Dictionary
    ##
    this_month = self.string_to_datetime(f'01/{invoice_ID}')
    x = calendar.monthrange(this_month.year, this_month.month)
    _, last_day = x
    end_date_of_this_month = f'{last_day}/{this_month.month}/{this_month.month}'
    ##
    self.display_horizontal_labels(parent, [
        'Bill to: ' +
        User_Dictionary.get('First_Name') + ' ' +
        User_Dictionary.get('Surname'),
        'Month Invoice: ' +
        Invoice_Dictionary.get('Month_Invoice_ID'),
        'Address: ' +
        User_Dictionary.get('Town') + ' ' +
        User_Dictionary.get('Post_Code') + ' ' +
        User_Dictionary.get('Home_Address'),
        'Invoice Due: ' +
        end_date_of_this_month
    ], start_row=0)
    list_of_labels = [
        "Order Placed Date",
        "Order ID",
        "Order Name",
        "Late Fees",
        "Shipping fees",
        "Order Total",
        "Payed",
    ]
    self.generate_line_labels(parent, list_of_labels, 5)


def generate_line_labels(self, parent, list_of_labels, start_row, start_index=0):
    i = 0 + start_index
    for label in list_of_labels:
        i += 1
        Label(parent, text=label).grid(column=i, row=start_row, padx=20)


def display_order_line_UI(self, __parent, Order_Dictionary):
    # DICTIONARIES
    Tool_Dictionary = self.tool_instance.fetch_tool_by_tool_id(
        Order_Dictionary.get('Unique_Item_Number'))
    Owner_Dictionary = self.user_instance.get_User_Dictionary_by_ID(
        Tool_Dictionary.get('Unique_User_ID'))
    # create parent
    PWparent = LabelFrame(__parent, text=Tool_Dictionary.get('Item_Name'))
    PWparent.grid()

    # Displayable Fees
    _pick_up_fee = self.get_displayable_price('0' if Order_Dictionary.get(
        'Pick_Up_Fee', '0') == '' else Order_Dictionary.get('Pick_Up_Fee', '0'))
    _drop_off_fee = self.get_displayable_price('0' if Order_Dictionary.get(
        'Drop_Off_Fee', '0') == '' else Order_Dictionary.get('Drop_Off_Fee', '0'))
    if(Order_Dictionary.get('Order_Type') == 'Full Day'):
        pass
    elif(Order_Dictionary.get('Order_Type') == 'Half Day'):
        pass
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5, sticky='we')
