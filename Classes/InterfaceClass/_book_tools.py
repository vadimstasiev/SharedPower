import uuid
import datetime
from tkinter import Label, LabelFrame, Button, Text, StringVar, IntVar, OptionMenu, Radiobutton, messagebox
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
    from Classes.tkinterwidgets.getfileswidget import GetImagesWidget, DisplayImagesWidget
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def user_view_all_tools_UI(self):
    self.go_back_menu = self.menu_user_options_UI
    self.reset_window()
    self.root.resizable(width=True, height=True)
    self.root.title("Shared Power - View Stock Inventory")
    self.add_menu_bar_UI_4()
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.minsize(1100, 700)
    sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
    # Get Results
    Results_List = self.tool_instance.fetch_all_listed_inventory()
    # Loop through all results and display them
    if len(Results_List) != 0:
        __i = 0
        for result_item in Results_List:
            __i += 1
            self.user_display_list_tool_UI(sc.container, result_item)
    else:
        Label(sc.container, text='Your inventory is empty',
              font=("Helvetica", 20)).grid(padx=100, pady=300)
    sc.grid(row=0, column=0, sticky='nsew')
    # Show any errors that might have come up
    self.generate_output_errors_UI(
        sc.container, padx=50, starting_index=500)
    self.root.mainloop()


def user_display_list_tool_UI(self, __parent, result_item, **kw):
    # create item dictionary
    Item_Dictionary = dict(
        zip(self.tool_instance.Inventory_Table_Index, result_item))
    # create parent
    PWparent = LabelFrame(__parent, text=Item_Dictionary.get('Item_Name'))
    # Get Image list
    returned_images = self.generate_PhotoImage_list(
        Item_Dictionary.get('Tool_Photos')
    )
    # Place photo if one exists
    if len(returned_images) > 0:
        # Display first image
        Label(PWparent, image=returned_images[0]).grid(
            rowspan=10, column=20, padx=20, pady=10)
    # Labels to display
    Owner_Dictionary = self.user_instance.get_User_Dictionary_by_ID(
        Item_Dictionary.get('Unique_User_ID')
    )
    _list = [
        'Half day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Half_Day_Fee')),
        'Full day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Full_Day_Fee')),
        'Current process state: ' +
        Item_Dictionary.get('Item_Process_State'),
        'Item Number: ' +
        Item_Dictionary.get('Unique_Item_Number'),
        'Owner: ' +
        Owner_Dictionary.get('First_Name') + ' ' +
        Owner_Dictionary.get('Surname'),
        'Town: ' + Owner_Dictionary.get('Town')
    ]
    self.display_horizontal_labels(PWparent, _list)
    # Place item description
    item_descrition = Text(PWparent, wrap='word', height=3, width=50)
    item_descrition.grid(row=3, column=2, pady=40, columnspan=2)
    # Get item description and trim it to fit the box
    _desc_amalgam = Item_Dictionary.get('Description', "error")
    _desc = _desc_amalgam.replace("\\n", " ").replace(
        "\\t", "").replace("''", "'")
    _max_char_len = 130
    if len(_desc) > _max_char_len:
        _new_desc = ""
        _word_list = _desc.split(" ")
        for _word in _word_list:
            if len(_new_desc) < _max_char_len:
                _new_desc += f" {_word}"
        _desc = _new_desc + " ( . . . ) "
    # Output item description
    item_descrition.insert('end', _desc)
    item_descrition.config(state='disabled')
    # View Tool item button
    viewB = Button(
        PWparent,
        text="View & Book",
        command=lambda: self.user_view_tool_UI(Item_Dictionary, Owner_Dictionary))
    viewB.grid(row=3, column=1, rowspan=2, padx=25, pady=10,
               ipadx=40, ipady=10, sticky='we')
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5, sticky='we')


def display_horizontal_labels(self, parent, _list, start_row=0):
    # Display labels in a 2 row x X column configuration
    _row_end = 1
    _column_offset = 1
    _list_len = len(_list)/2 + _column_offset
    _column_start = _column_offset
    _column_end = int(_list_len)
    if _column_end % 2 == 1:
        case = "uneven"
        _column_end += 1
    else:
        case = "even"
    _index = 0
    # Add the Horizontal Labels

    def add_Label(__text, _column, _row):
        Label(parent, text=__text).grid(
            row=_row, column=_column, padx=30, sticky="nw")
    for _i in range(_column_start, _column_end):
        for _j in range(0+start_row, _row_end+1+start_row):
            if case == "even":
                add_Label(_list[_index], _i, _j)
            elif case == "uneven":
                if _index < len(_list):
                    add_Label(_list[_index], _i, _j)
            _index += 1


def user_view_tool_UI(self, Item_Dictionary, Owner_Dictionary):
    self.go_back_menu = self.user_view_all_tools_UI
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - View Tool")
    self.add_menu_bar_UI_4()
    # create parent
    LBtext = Item_Dictionary.get("Item_Name")
    PWparent = LabelFrame(
        self.root_frame,
        text=LBtext
    )
    self.display_horizontal_labels(PWparent, [
        'Owner: ' +
        Owner_Dictionary.get('First_Name') + ' ' +
        Owner_Dictionary.get('Surname'),
        'Town: ' + Owner_Dictionary.get('Town'),
        'Half day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Half_Day_Fee')),
        'Full day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Full_Day_Fee')),
        'Pick up fee: ' +
        self.get_displayable_price(Item_Dictionary.get('Pick_Up_Fee')),
        'Drop off fee: ' +
        self.get_displayable_price(Item_Dictionary.get('Drop_Off_Fee'))
    ], start_row=0)

    self.display_horizontal_labels(PWparent, [
        'Process State: ' +
        Item_Dictionary.get('Item_Process_State', 'Error'),
        'Item Number: ' +
        Item_Dictionary.get('Unique_Item_Number'),
        'Availability start date: ' +
        Item_Dictionary.get('Availability_Start_Date'),
        'Availability end date: ' +
        Item_Dictionary.get('Availability_End_Date')
    ], start_row=2)
    _descL = Label(PWparent, text="Description: ")
    _descL.grid(row=4, column=0)
    description_box = Text(PWparent, wrap='word', height=10, width=80)
    description_box.grid(row=4, column=1, columnspan=5)
    _desc = Item_Dictionary.get('Description', "error").replace(
        '\\t', '').replace('\\n', ' \n').replace("''", "'")
    description_box.insert('end', _desc)

    _viewbookingsB = Button(
        PWparent,
        text='View Bookings',
        command=lambda: self.view_bookings_Calendar_UI(Item_Dictionary)
    )
    _viewbookingsB.grid(row=6, column=1, columnspan=2, sticky='w')
    # Date entries vars and labels
    start_date_StrVar = StringVar()
    end_date_StrVar = StringVar()
    start_date_l = Label(PWparent, text="Start Date:")
    end_date_l = Label(PWparent, text="End Date:")

    dateentry1 = self.place_date_entry_get_entry(PWparent, start_date_StrVar)
    dateentry2 = self.place_date_entry_get_entry(PWparent, end_date_StrVar)
    # forget by default
    dateentry1.grid_forget()
    dateentry2.grid_forget()

    choices = {'6:00-12:00', '12:00-18:00'}
    default_selection = 'Please Select'
    hours_StrVar = StringVar()
    hours_StrVar.set(default_selection)
    times_select = OptionMenu(
        PWparent,
        hours_StrVar,  # TODO grab this
        *choices
    )

    # Fee Buttons
    feesIntVar = IntVar()
    type_of_deliveryBtn1 = Radiobutton(
        PWparent, text="Delivery to home address (Adds Fees)", padx=20, variable=feesIntVar, value=0)
    type_of_deliveryBtn2 = Radiobutton(
        PWparent, text="Collection by User", padx=20, variable=feesIntVar, value=1)

    # Submit button
    BookB = Button(
        PWparent,
        text='Book Tool',
        command=lambda: self.process_book_tool(
            PWparent,
            Item_Dictionary,
            type_of_booking=type_of_booking_StrVar.get(),
            start_date=start_date_StrVar.get(),
            end_date=end_date_StrVar.get(),
            order_hours=hours_StrVar.get(),
            fees_int=feesIntVar.get(),
            tool_ID=Item_Dictionary.get('Unique_Item_Number'),
            owner_ID=Item_Dictionary.get('Unique_User_ID')
        )
    )

    def show_hide_date_input(ignoreevent):
        if(type_of_booking_StrVar.get() == 'Full Day'):
            start_date_l.grid(row=8, column=0, sticky='w')
            dateentry1.grid(row=8, column=1, columnspan=2, sticky='w')
            end_date_l.grid(row=9, column=0, sticky='w')
            dateentry2.grid(row=9, column=1, columnspan=2, sticky='w')
            times_select.grid_forget()
            start_date_l.config(text="Start Date:")

        if(type_of_booking_StrVar.get() == 'Half Day'):
            start_date_l.grid_forget()
            start_date_l.config(text="Date:")
            dateentry1.grid_forget()
            end_date_l.grid_forget()
            dateentry2.grid_forget()
            start_date_l.grid(row=8, column=0, sticky='w')
            dateentry1.grid(row=8, column=1, columnspan=2, sticky='w')
            times_select.grid(row=10, column=1, columnspan=2,
                              sticky='w', pady=5)
        type_of_deliveryBtn1.grid(
            row=11, column=1, columnspan=2, sticky='w', pady=5)
        type_of_deliveryBtn2.grid(
            row=12, column=1, columnspan=2, sticky='w', pady=5)
        BookB.grid(row=13, column=1, columnspan=2, sticky='w', pady=5)

    # Booking  Label
    Label(PWparent, text="Book Now:").grid(
        row=7, column=0, sticky='w', pady=5)
    # Type of booking Half Day or Full Day select
    choices = {'Half Day', 'Full Day'}
    default_selection = 'Please Select'
    type_of_booking_StrVar = StringVar()
    type_of_booking_StrVar.set(default_selection)
    dropdown_select = OptionMenu(
        PWparent,
        type_of_booking_StrVar,
        command=show_hide_date_input,
        *choices
    )
    dropdown_select.grid(row=7, column=1, columnspan=2, sticky='w', pady=5)

    # Custom GetImagesWidget
    images_path_list = self.unpack_db_images_path(
        Item_Dictionary.get('Tool_Photos', ''))
    images_widget = DisplayImagesWidget(
        PWparent, empty_message='No Photo', max_items=3)
    # Get Tool ID number
    images_widget.grid(row=5, column=1, columnspan=2, sticky='w')
    images_widget.automatic__file_input(images_path_list)
    # Place Parent
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
    self.root.mainloop()


def process_book_tool(self, parent, Tool_Dictionary, **kwargs):
    self.clear_errors()
    User_Dictionary = self.user_instance.User_Dictionary
    self.validate_booking(User_Dictionary, **kwargs)
    if len(self.buffered_errors) == 0:
        if kwargs.get('fees_int', '') == 1:
            pick_up_fee = '0'
        else:
            pick_up_fee = Tool_Dictionary.get('Pick_Up_Fee')

        answer = messagebox.askyesnocancel(
            "Book Tool",
            "Are you sure that you want to make this booking?",
            icon='warning'
        )
        if answer == 1:
            self.order_instance.record_order(
                Unique_Order_ID=str(int(uuid.uuid1())),
                Unique_Item_Number=Tool_Dictionary.get('Unique_Item_Number'),
                Unique_User_ID=User_Dictionary.get('Unique_User_ID'),
                Order_Date=self.datetime_to_string(datetime.datetime.now()),
                Pick_Up_Fee=pick_up_fee,
                Order_Type=kwargs.get('type_of_booking'),
                Order_Hours=kwargs.get('order_hours'),
                Booking_Start_Day=kwargs.get('start_date'),
                Booking_End_Day=kwargs.get('end_date')
            )
            messagebox.showinfo(
                title='Success', message='Success! Tool Booked')
    self.generate_output_errors_UI(parent, starting_index=30)


def validate_booking(self, User_Dictionary, **kwargs):
    date_conflict = False
    tool_ID = kwargs.get('tool_ID')
    OrdersList = self.order_instance.fetch_orders_from_tool_id(tool_ID)
    start_datetime = self.string_to_datetime(kwargs.get('start_date'))
    end_datetime = self.string_to_datetime(kwargs.get('end_date'))
    booking_type = kwargs.get('type_of_booking')
    booking_hours = kwargs.get('order_hours')
    for order in OrdersList:
        # get values
        OrderDictionary = dict(
            zip(self.order_instance.orders_table_Index, order)
        )
        order_type = OrderDictionary.get('Order_Type')
        order_start_datetime = self.string_to_datetime(
            OrderDictionary.get('Booking_Start_Day')
        )
        order_hours = OrderDictionary.get('Order_Hours')
        order_end_datetime = None
        try:
            order_end_datetime = self.string_to_datetime(
                OrderDictionary.get('Booking_End_Day')
            )
        except:
            pass
        # check validity
        if order_type == 'Full Day':
            if booking_type == 'Full Day':
                if order_start_datetime <= start_datetime <= order_end_datetime:
                    date_conflict = True
                elif order_start_datetime <= end_datetime <= order_end_datetime:
                    date_conflict = True
            elif booking_type == 'Half Day':
                if order_start_datetime <= start_datetime <= order_end_datetime:
                    date_conflict = True
                if start_datetime > end_datetime:
                    self.buffered_errors.append(
                        'Ending date cannot be before starting date')
        elif order_type == 'Half Day':
            if booking_type == 'Full Day':
                if order_start_datetime == start_datetime:
                    date_conflict = True
                elif order_start_datetime == end_datetime:
                    date_conflict = True
            elif booking_type == 'Half Day':
                if order_start_datetime == start_datetime:
                    if order_hours == booking_hours:
                        date_conflict = True
                    if start_datetime > end_datetime:
                        self.buffered_errors.append(
                            'Ending date cannot be before starting date')

    if date_conflict == True:
        self.buffered_errors.append(
            'Booking conflicts with existing order')
    elif (end_datetime-start_datetime).days >= 3:
        self.buffered_errors.append(
            'You cannot book the tool for longer than 3 days')
    elif kwargs.get('order_hours') == 'Please Select' and kwargs.get('type_of_booking') == 'Half Day':
        self.buffered_errors.append('Please select the half day hours')
    elif User_Dictionary.get('Unique_User_ID') == kwargs.get('owner_ID'):
        self.buffered_errors.append('You cannot book your own tool')
    elif (start_datetime-datetime.datetime.now()).days/7 >= 6:
        self.buffered_errors.append(
            'You cannot book earlier than 6 weeks in advance')
