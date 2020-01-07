import datetime
from tkinter import Label, LabelFrame, Entry, Text, Button, StringVar, OptionMenu, messagebox
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
    from Classes.tkinterwidgets.getfileswidget import GetImagesWidget, DisplayImagesWidget
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def view_listed_inventory_UI(self):
    self.go_back_menu = self.menu_user_options_UI
    self.reset_window()
    self.root.resizable(width=True, height=True)
    self.root.title("Shared Power - View Stock Inventory")
    self.add_menu_bar_UI_4()
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.minsize(900, 700)
    sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
    # Get Results
    User_ID = self.user_instance.get_user_unique_ID()
    results_list = self.tool_instance.fetch_user_listed_inventory(User_ID)
    # Loop through all results and display them
    if len(results_list) != 0:
        __i = 0
        for result_item in results_list:
            __i += 1
            self.display_list_tool_UI(sc.container, result_item)
    else:
        Label(sc.container, text='Your inventory is empty',
              font=("Helvetica", 20)).grid(padx=100, pady=300)
    sc.grid(row=0, column=0, sticky='nsew')
    # Show any errors that might have come up
    self.generate_output_errors_UI(sc.container, padx=50, starting_index=500)
    self.root.mainloop()


def display_list_tool_UI(self, __parent, result_item, **kw):
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
            rowspan=4, padx=20, pady=10)
    # Labels to display
    _list = [
        'Half day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Half_Day_Fee')),
        'Full day rate: ' +
        self.get_displayable_price(Item_Dictionary.get('Full_Day_Fee')),
        'Current process state: ' + Item_Dictionary.get('Item_Process_State'),
        'Item Number: ' + Item_Dictionary.get('Unique_Item_Number')
    ]
    # Display labels in a 2 row x X column configuration
    _row_end = 1
    _column_offset = 1
    _list_len = len(_list)/2 + _column_offset
    _column_start = _column_offset
    _column_end = int(_list_len)
    if _column_end != _list_len:
        case = "uneven"
        _column_end += 1
    else:
        case = "even"

    def add_Label(__text, _column, _row):
        Label(PWparent, text=__text).grid(
            row=_row, column=_column, padx=30, sticky="nw")
    _index = 0
    for _i in range(_column_start, _column_end):
        for _j in range(0, _row_end+1):
            if case == "even":
                add_Label(_list[_index], _i, _j)
            elif case == "uneven":
                if(_i != _column_end):
                    add_Label(_list[_index], _i, _j)
            _index += 1
    # Place item description
    item_descrition = Text(PWparent, wrap='word', height=3, width=50)
    item_descrition.grid(row=3, column=1, columnspan=100)
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
    # View/Edit item button
    viewB = Button(
        PWparent,
        text="View Tool",
        command=lambda: self.owner_edit_view_individual_tool_UI(Item_Dictionary, read_only=True))
    viewB.grid(column=30, row=0, rowspan=2, pady=10,
               ipadx=40, ipady=2, sticky='we')
    editB = Button(
        PWparent,
        text="Edit Tool",
        command=lambda: self.owner_edit_view_individual_tool_UI(Item_Dictionary))
    editB.grid(column=30, row=2, rowspan=2, pady=10,
               ipadx=40, ipady=2, sticky='we')
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5, sticky='we')


def owner_edit_view_individual_tool_UI(self, Item_Dictionary, read_only=False):
    self.go_back_menu = self.view_listed_inventory_UI
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - Tool")
    self.add_menu_bar_UI_4()
    # create parent
    LBtext = "Edit Tool: " + Item_Dictionary.get("Item_Name")
    PWparent = LabelFrame(
        self.root_frame,
        text=LBtext
    )
    # StrVars
    toolname_StrVar = StringVar()
    half_rate_StrVar = StringVar()
    full_rate_StrVar = StringVar()
    start_date_StrVar = StringVar()
    end_date_StrVar = StringVar()
    process_state_StrVar = StringVar()
    # Generate Labels and Entries
    _, entries_list = self.generate_labels_and_entries_UI(PWparent, [
        ("Tool Name:", toolname_StrVar),  # 0
        ("Description:", None),  # 1
        ("Half day rate:", half_rate_StrVar),  # 2
        ("Full Day Rate:", full_rate_StrVar),  # 3
        ("Availability start date:", None),  # 4
        ("Availablity end date:", None),  # 5
        ("Dates Booked:", None),  # 6
        ("Item Process State:", None),  # 7
        ("Choose Photo:", None),  # 8
    ])
    # Fill the empty Entries
    entries_list[0].insert(0, Item_Dictionary.get("Item_Name"))
    entries_list[2].insert(0, self.get_displayable_price(
        Item_Dictionary.get("Half_Day_Fee")))
    entries_list[3].insert(0, self.get_displayable_price(
        Item_Dictionary.get("Full_Day_Fee")))
    # Description Textbox
    description_box = Text(PWparent, wrap='word', height=10, width=80)
    description_box.grid(row=1, column=1, columnspan=5)
    _desc = Item_Dictionary.get('Description', "error").replace(
        '\\t', '').replace('\\n', ' \n').replace("''", "'")
    description_box.insert('end', _desc)
    # Date entry start date
    start_datetime = self.string_to_datetime(
        Item_Dictionary.get("Availability_Start_Date"))
    start_dateentry = self.place_date_entry_get_entry(
        PWparent,
        start_date_StrVar,
        row=4, column=1,
        columnspan=2, sticky='w',
        date=start_datetime
    )
    if start_datetime < datetime.datetime.now():
        start_dateentry.config(state='disabled')
        _message = Label(
            PWparent, text="Not editable if tool was once already available")
        _message.grid(row=4, column=3, sticky='w')
    # Date entry end date
    end_datetime = self.string_to_datetime(
        Item_Dictionary.get("Availability_End_Date"))
    end_dateentry = self.place_date_entry_get_entry(
        PWparent,
        end_date_StrVar,
        row=5, column=1,
        columnspan=2, sticky='w',
        date=end_datetime
    )
    # if len( THERE ARE ANY BOOKING ALREADY) > 1: # TODO
    #     end_dateentry.config(state='disabled')
    #     _message = Label(
    #         PWparent, text="Not editable if tool was once already booked")
    #     _message.grid(row=5, column=3, sticky='w')
    # View bookings
    _viewbookingsB = Button(
        PWparent,
        text='View Bookings',
        # command=lambda: self.view_bookings_Calendar_UI(Availability_Pair_List) # TODO NEED TO GET BOOKING SYSTEM DONE
    )
    _viewbookingsB.grid(row=6, column=1, columnspan=2, sticky='w')
    # Dropdown select
    choices = {'with owner', 'with depot', 'with user',
               'with insurance', 'being processed'}
    default_selection = Item_Dictionary.get(
        'Item_Process_State', 'Error')
    process_state_StrVar.set(default_selection)
    dropdown_select = OptionMenu(PWparent, process_state_StrVar, *choices)
    dropdown_select.grid(row=7, column=1, columnspan=2, sticky='w', pady=5)
    # Custom GetImagesWidget
    images_path_list = self.unpack_db_images_path(
        Item_Dictionary.get('Tool_Photos', ''))
    images_widget = GetImagesWidget(
        PWparent, empty_message='Add Photo', max_items=3)
    # Get Tool ID number
    tool_ID = Item_Dictionary.get("Unique_Item_Number")
    # Read-only Mode - Disable input on EVERYTHING
    if read_only == True:
        for entry in entries_list:
            if type(entry) == type(Entry()):
                entry.config(state='disabled')
        description_box.config(state='disabled')
        start_dateentry.config(state='disabled')
        end_dateentry.config(state='disabled')
        dropdown_select.config(state='disabled')
        images_widget = DisplayImagesWidget(
            PWparent, empty_message='Not Available')
    else:
        # Place Buttons
        _updateinfoB = Button(
            PWparent,
            text="Update Tool Information",
            command=lambda: self.process_register_or_update_tool(
                PWparent,
                Tool_ID=tool_ID,
                Tool_Name=toolname_StrVar,
                Description_Box=description_box,
                Half_Day_Rate=half_rate_StrVar,
                Full_Day_Rate=full_rate_StrVar,
                Start_Date=start_date_StrVar,
                End_Date=end_date_StrVar,
                Images_Widget=images_widget,
                Process_State=process_state_StrVar,
                Update=True
            )
        )
        _updateinfoB.grid(column=5, ipadx=10, ipady=5, sticky='e')
        _removelisting = Button(
            PWparent,
            text="Remove Tool Listing",
            command=lambda: self.delete_tool(tool_ID, images_path_list),
        )
        _removelisting.grid(column=5, ipadx=10, ipady=5, sticky='e')
    # Place images_widget
    images_widget.grid(row=8, column=1, columnspan=2, sticky='w')
    images_widget.automatic__file_input(images_path_list)
    # Place Parent
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
    self.root.mainloop()


def delete_tool(self, tool_ID, images_to_delete):
    answer = messagebox.askyesnocancel(
        "Delete Tool Listing",
        "Are you sure that you want to remove this listing?",
        icon='warning'
    )
    if answer == 1:
        self.user_instance.delete_tool(tool_ID)
        self.delete_images(images_to_delete)
        self.go_back_menu()
