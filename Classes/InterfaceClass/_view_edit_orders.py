import datetime
from tkinter import Label, LabelFrame, Frame, Entry, Text, Button, StringVar, OptionMenu, messagebox, Toplevel
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.scrollablecontainer import ScrollableContainer
    from Classes.tkinterwidgets.getfileswidget import GetImagesWidget, DisplayImagesWidget
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def view_listed_orders_UI(self):  # TODO display ordeers by tool ID - for owners
    self.go_back_menu = self.menu_user_options_UI
    self.reset_window()
    self.root.resizable(width=True, height=True)
    self.root.title("Shared Power - View Orders")
    self.add_menu_bar_UI_4()
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    self.root.minsize(1250, 700)
    sc = ScrollableContainer(self.root, bd=2, scroll='vertical')
    # Get Results
    User_ID = self.user_instance.get_user_unique_ID()
    orders_list = self.order_instance.fetch_orders_from_user_id(User_ID)
    # Loop through all results and display them
    __i = 0
    display_list = []
    for order in orders_list:
        __i += 1
        Order_Dictionary = dict(
            zip(self.order_instance.orders_table_Index, order))
        if Order_Dictionary.get('Order_State') == 'Not_Complete':
            display_list.append(order)
    if len(display_list) != 0:
        for _order in display_list:
            Order_Dictionary = dict(
                zip(self.order_instance.orders_table_Index, _order))
            self.display_order_UI(sc.container, Order_Dictionary)
    else:
        Label(sc.container, text="You don't have any orders orders",
              font=("Helvetica", 20)).grid(padx=100, pady=300)
    sc.grid(row=0, column=0, sticky='nsew')
    # Show any errors that might have come up
    self.generate_output_errors_UI(sc.container, padx=50, starting_index=500)
    self.root.mainloop()


def display_order_UI(self, __parent, Order_Dictionary, **kw):
    # prepare the necessary dictionaries
    Tool_Dictionary = self.tool_instance.fetch_tool_by_tool_id(
        Order_Dictionary.get('Unique_Item_Number'))
    Owner_Dictionary = self.user_instance.get_User_Dictionary_by_ID(
        Tool_Dictionary.get('Unique_User_ID'))
    # create parent
    PWparent = LabelFrame(__parent, text=Tool_Dictionary.get('Item_Name'))
    # Get Image list
    returned_images = self.generate_PhotoImage_list(
        Tool_Dictionary.get('Tool_Photos')
    )
    # Place photo if one exists
    if len(returned_images) > 0:
        # Display first image
        Label(PWparent, image=returned_images[0]).grid(
            column=30, row=2, rowspan=10, padx=20, pady=10)
    # Labels Parent
    # PWparent = Frame(PWparent)
    # PWparent.grid(column=1)
    # get fees
    _pick_up_fee = self.get_displayable_price('0' if Order_Dictionary.get(
        'Pick_Up_Fee', '0') == '' else Order_Dictionary.get('Pick_Up_Fee', '0'))
    _drop_off_fee = self.get_displayable_price('0' if Order_Dictionary.get(
        'Drop_Off_Fee', '0') == '' else Order_Dictionary.get('Drop_Off_Fee', '0'))
    if(Order_Dictionary.get('Order_Type') == 'Full Day'):
        # Display labels in a 2 row x X column configuration
        self.display_horizontal_labels(PWparent, [
            'Booking Type: ' + Order_Dictionary.get('Order_Type'),
            'Current Process State: ' +
            Tool_Dictionary.get('Item_Process_State'),
            'Booked Pick-Up Date: ' +
            Order_Dictionary.get('Booking_Start_Day'),
            'Booked Drop-Off Date: ' +
            Order_Dictionary.get('Booking_End_Day'),
        ], start_row=0)
    else:  # Half Day
        # Display labels in a 2 row x X column configuration
        self.display_horizontal_labels(PWparent, [
            'Booking Type: ' + Order_Dictionary.get('Order_Type'),
            'Current process state: ' +
            Tool_Dictionary.get('Item_Process_State'),
            'Booked Date: ' +
            Order_Dictionary.get('Booking_Start_Day'),
            'Booked Hours: ' + Order_Dictionary.get('Order_Hours'),
        ], start_row=0)
    # Display labels in a 2 row x X column configuration
    self.display_horizontal_labels(PWparent, [
        'Order Date: ' + Order_Dictionary.get('Order_Date'),
        'Item Number: ' + Order_Dictionary.get('Unique_Item_Number'),
        'Order Number: ' + Order_Dictionary.get('Unique_Order_ID'),
        'Owner ID Number: ' + Tool_Dictionary.get('Unique_User_ID'),
    ], start_row=2)
    self.display_horizontal_labels(PWparent, [
        'Pick-Up Fee: ' + _pick_up_fee,
        'Drop-Off Fee: ' + _drop_off_fee,
        'Owner: ' +
        Owner_Dictionary.get('First_Name') + ' ' +
        Owner_Dictionary.get('Surname'),
    ], start_row=4)
    # View/Edit item button
    if Tool_Dictionary.get('Item_Process_State', 'Error') == 'with user':
        viewB = Button(
            PWparent,
            text="Return or Arrange Collection",
            # command=lambda: self.owner_edit_view_individual_order_UI(Order_Dictionary, Tool_Dictionary))
            command=lambda: self.return_or_arrange_collection(Order_Dictionary, Tool_Dictionary))
    else:
        viewB = Button(
            PWparent,
            text="Mark as Received",
            command=lambda: self.mark_as_received(Order_Dictionary)
        )

    viewB.grid(column=0, row=0, rowspan=2, pady=10, padx=25,
               ipadx=40, ipady=2, sticky='we')
    editB = Button(
        PWparent,
        text="Cancel Order",
        command=lambda: self.owner_edit_view_individual_order_UI(Order_Dictionary, Tool_Dictionary))
    editB.grid(column=0, row=2, rowspan=2, pady=10, padx=25,
               ipadx=40, ipady=2, sticky='we')
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5, sticky='we')


# Dispach/Arrange Collection Here

def return_or_arrange_collection(self, Order_Dictionary, Tool_Dictionary):
    top = Toplevel(self.root)
    Button(
        top,
        text="Return to Owner",
        command=lambda: self.mark_as_returned_to_owner(
            Order_Dictionary, 'owner'),
    ).pack(fill="both", expand=True)
    Button(
        top,
        text="Return",
        command=lambda: self.mark_as_returned_to_owner(
            Order_Dictionary, 'depot'),
    ).pack(fill="both", expand=True)
    Button(
        top,
        text="Arrange Collection - Deliver to Depot",
        command=lambda: self.mark_as_received(Order_Dictionary),
    ).pack(fill="both", expand=True)


def mark_as_returned_to_owner(self, Order_Dictionary, returnto):
    if returnto == 'owner':
        self.tool_instance.update_tool(
            Unique_Item_Number=Order_Dictionary.get('Unique_Item_Number'),
            Item_Process_State='with owner'
        )
    elif returnto == 'depot':
        self.tool_instance.update_tool(
            Unique_Item_Number=Order_Dictionary.get('Unique_Item_Number'),
            Item_Process_State='with depot'
        )
    self.view_listed_orders_UI()

# mark item as locked if it was already delivered


def mark_as_returned_to_depot(self,  Order_Dictionary):
    self.tool_instance.update_tool(
        Unique_Item_Number=Order_Dictionary.get('Unique_Item_Number'),
        Item_Process_State='with depot'
    )

# Mark as received Here


def mark_as_received(self, Order_Dictionary):
    self.tool_instance.update_tool(
        Unique_Item_Number=Order_Dictionary.get('Unique_Item_Number'),
        Order_State='Complete',
        Item_Process_State='with user'
    )
    self.view_listed_orders_UI()


def owner_edit_view_individual_order_UI(self, Order_Dictionary, Tool_Dictionary):
    self.go_back_menu = self.view_listed_orders_UI
    self.reset_window()
    self.root.resizable(width=False, height=False)
    self.root.title("Shared Power - Tool")
    self.add_menu_bar_UI_4()
    # create parent
    LBtext = "Edit Tool: " + Tool_Dictionary.get("Item_Name")
    PWparent = Frame(
        self.root_frame
    )
    # Order ID
    order_ID = Order_Dictionary.get("Unique_Order_ID")

    # StrVars
    drop_off_fee_StrVar = StringVar()
    feedback_StrVar = StringVar()
    # Dropdown select
    choices = {'with owner', 'with depot', 'with user',
               'with insurance', 'being processed'}
    default_selection = Tool_Dictionary.get('Item_Process_State', 'Error')
    process_state_StrVar = StringVar()
    process_state_StrVar.set(default_selection)
    Label(PWparent, text="Item Process State:").grid(row=0, column=0)

    # Custom GetImagesWidget
    images_widget = GetImagesWidget(
        PWparent, empty_message='Add Photo', max_items=3)

    customer_feedback_box = Text(PWparent)
    customer_feedback_label = Label(PWparent, text="Feedback:")
    condition_photos_label = Label(PWparent, text="Tool Condition Photos:")

    def show_and_hide_elements(ignoreevent):
        orvar = False
        if process_state_StrVar.get() == 'with depot':
            orvar = True
        elif process_state_StrVar.get() == 'with owner':
            orvar = True
        if orvar == True:
            customer_feedback_label.grid(row=9, column=0)
            customer_feedback_box.grid(
                row=9, column=1, columnspan=2, sticky='w')
            condition_photos_label.grid(row=10, column=0)
            images_widget.grid(row=10, column=1, columnspan=2, sticky='w')
        else:
            customer_feedback_box.grid_forget()
            images_widget.grid_forget()
            customer_feedback_label.grid_forget()
            condition_photos_label.grid_forget()
    dropdown_select = OptionMenu(
        PWparent,
        process_state_StrVar,
        command=show_and_hide_elements,
        *choices
    )
    dropdown_select.grid(row=0, column=1, columnspan=2, sticky='w', pady=5)
    # Place Buttons
    _updateinfoB = Button(
        PWparent,
        text="Update Tool Information",
        command=lambda: self.process_register_or_update_tool(
            PWparent,
            Order_ID=order_ID,
            Drop_Off_Fee=drop_off_fee_StrVar,
            Process_State=process_state_StrVar,
            Customer_Feedback=feedback_StrVar,
            Customer_Condition_Photos=images_widget,
            Update=True
        )
    )
    _updateinfoB.grid(column=5, ipadx=10, ipady=5, sticky='e')
    # Place Parent
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5)
    self.root.mainloop()


def delete_order(self, tool_ID, images_to_delete):
    answer = messagebox.askyesnocancel(
        "Delete Tool Listing",
        "Are you sure that you want to remove this listing?",
        icon='warning'
    )
    if answer == 1:
        self.user_instance.delete_order(tool_ID)
        self.go_back_menu()
