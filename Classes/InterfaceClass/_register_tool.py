import uuid
from tkinter import StringVar, LabelFrame, Button, Text
from Classes.MoneyParser import price_dec
from Classes.tkinterwidgets.getfileswidget import GetImagesWidget
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass


def register_tool_UI(self):
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - Register New Tool")
    self.add_menu_bar_UI_4()
    PWparent = LabelFrame(self.root_frame, text="Register Tool")
    # StrVars
    toolname_StrVar = StringVar()
    half_rate_StrVar = StringVar()
    full_rate_StrVar = StringVar()
    pick_up_fee_StrVar = StringVar()
    drop_off_fee_StrVar = StringVar()
    # Labels and entries
    self.generate_labels_and_entries_UI(PWparent, [
        ("Tool Name:", toolname_StrVar),
        ("Description:", None),
        ("Half day rate:", half_rate_StrVar),
        ("Full Day Rate:", full_rate_StrVar),
        ("Pick Up Fee:", pick_up_fee_StrVar),
        ("Drop Off Fee:", drop_off_fee_StrVar),
        ("Availablity start date:", None),
        ("Availablity end date:", None),
        ("Choose Photo:", None),
    ])
    # Description Box
    description_box = Text(
        PWparent,
        wrap='word',
        height=10,
        width=80
    )
    description_box.grid(row=1, column=1, columnspan=5)
    # Start date Widget
    start_date_StrVar = StringVar()
    self.place_date_entry_get_entry(
        PWparent, start_date_StrVar, row=6, column=1, columnspan=2, sticky='w')
    # End date Widget
    end_date_StrVar = StringVar()
    self.place_date_entry_get_entry(
        PWparent, end_date_StrVar, row=7, column=1, columnspan=2, sticky='w')
    # Get Photo Widget
    images_widget = GetImagesWidget(
        PWparent, empty_message='Add Photo', max_items=3)
    images_widget.grid(row=8, column=1, columnspan=2, sticky='w')
    # Variable Dictionary
    VariableDict = {
        "Tool_Name": toolname_StrVar,
        "Description_Box": description_box,
        "Half_Day_Rate": half_rate_StrVar,
        "Full_Day_Rate": full_rate_StrVar,
        "Pick_Up_Fee": pick_up_fee_StrVar,
        "Drop_Off_Fee": drop_off_fee_StrVar,
        "Start_Date": start_date_StrVar,
        "End_Date": end_date_StrVar,
        "Images_Widget": images_widget
    }
    # Register Button
    registerB = Button(
        PWparent,
        text="Register",
        command=lambda: self.process_register_or_update_tool(
            PWparent, **VariableDict)
    )
    registerB.grid(column=5, ipadx=10, ipady=5)
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
    self.go_back_menu = self.menu_user_options_UI
    self.root.mainloop()


def process_register_or_update_tool(self, _parent, **kw):  # TODO TODO TODO
    # Class Vars, some are public so they can be easily validated
    R_user_ID = self.user_instance.get_user_unique_ID()
    # Get defined tool_ID or generate one based on uuid1
    R_tool_ID = kw.pop("Tool_ID", str(int(uuid.uuid1())))
    self.R_tool_name = str(kw.pop("Tool_Name").get())
    self.R_description = str(
        kw.pop("Description_Box").get("1.0", 'end-1c')
    ).replace("'", "''")
    # Get day rates
    self.R_half_day_rate = str(kw.pop("Half_Day_Rate").get())
    self.R_full_day_rate = str(kw.pop("Full_Day_Rate").get())
    self.R_pick_up_fee = str(kw.pop("Pick_Up_Fee").get())
    self.R_drop_off_fee = str(kw.pop("Drop_Off_Fee").get())
    # Get or Set default Process State
    process_state = kw.pop("Process_State", StringVar()).get()
    if process_state != "":
        self.R_process_state = str(process_state)
    else:
        self.R_process_state = "with owner"
    # Get Dates
    R_start_date = kw.pop("Start_Date").get()
    R_end_date = kw.pop("End_Date").get()
    # Check wether to update or register
    Update = kw.pop("Update", False)
    # Validate Vars
    self.validate_register_tool_input()
    # Check if Vars produced any errors
    if(len(self.buffered_errors) == 0):
        self.clear_errors()
        images_widget = kw.get("Images_Widget")
        R_packed_images = self.get_image_paths_str_DB_ready(images_widget)
        kwargs = {
            'Unique_Item_Number': R_tool_ID,
            'Unique_User_ID': R_user_ID,
            'Item_Name': self.R_tool_name,
            'Half_Day_Fee': self.get_savable_int_price(self.R_half_day_rate),
            'Full_Day_Fee': self.get_savable_int_price(self.R_full_day_rate),
            'Pick_Up_Fee': self.get_savable_int_price(self.R_pick_up_fee),
            'Drop_Off_Fee': self.get_savable_int_price(self.R_drop_off_fee),
            'Description': self.R_description,
            'Availability_Start_Date': R_start_date,
            'Availability_End_Date': R_end_date,
            'Item_Process_State': self.R_process_state,
            'Tool_Photos': R_packed_images
        }
        if Update:
            self.tool_instance.update_tool(**kwargs)
        else:
            self.tool_instance.register_tool(**kwargs)
        self.go_back_menu()
    else:
        self.clear_errors()
        self.generate_output_errors_UI(
            _parent, column=0,
            starting_index=100,
            padx=50, sticky='se'
        )


def validate_register_tool_input(self):
    if(self.R_tool_name == ""):
        self.buffered_errors.append(
            "Please enter the tool name")
    if(self.R_description == ""):
        self.buffered_errors.append(
            "Please enter a description")
    if self.R_half_day_rate == 0:
        self.buffered_errors.append(
            "Please enter the half day rate")
    try:
        price_dec(self.R_half_day_rate)
    except:
        self.buffered_errors.append(
            "Please enter a valid price for the half day rate")
    if self.R_full_day_rate == 0:
        self.buffered_errors.append(
            "Please enter the full day rate")
    try:
        price_dec(self.R_full_day_rate)
    except:
        self.buffered_errors.append(
            "Please enter a valid price for the full day rate")
    if self.R_pick_up_fee == 0:
        self.buffered_errors.append(
            "Please enter the pick up fee")
    try:
        price_dec(self.R_pick_up_fee)
    except:
        self.buffered_errors.append(
            "Please enter a valid price for the pick up fee")
    if self.R_drop_off_fee == 0:
        self.buffered_errors.append(
            "Please enter the drop off fee")
    try:
        price_dec(self.R_drop_off_fee)
    except:
        self.buffered_errors.append(
            "Please enter a valid price for the drop off fee")
