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
        Label(sc.container, text="You don't have any orders",
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
    if self.string_to_datetime(Order_Dictionary.get('Booking_Start_Day')) <= datetime.datetime.now():
        tool_process_state = Tool_Dictionary.get('Item_Process_State', 'Error')
        orvar = False
        if tool_process_state == 'with owner':
            orvar = True
        elif tool_process_state == 'with depot':
            orvar = True
        if orvar:
            viewB = Button(
                PWparent,
                text="Mark as Received",
                command=lambda: self.mark_as_received(Order_Dictionary)
            )
        elif tool_process_state == 'with user':
            viewB = Button(
                PWparent,
                text="Return or Arrange Collection",
                command=lambda: self.return_or_arrange_collection(Order_Dictionary, Tool_Dictionary))
        else:
            editB = Button(
                PWparent,
                text="Cancel Order",
                command=lambda: self.cancel_order(Order_Dictionary, Tool_Dictionary))
            editB.grid(column=0, row=2, rowspan=2, pady=10, padx=25,
                       ipadx=40, ipady=2, sticky='we')
        viewB.grid(column=0, row=0, rowspan=2, pady=10, padx=25,
                   ipadx=40, ipady=2, sticky='we')
    PWparent.grid(ipadx=50, ipady=30, padx=5, pady=5, sticky='we')


# Dispach/Arrange Collection Here

def return_or_arrange_collection(self, Order_Dictionary, Tool_Dictionary):
    top = Toplevel(self.root)
    top.attributes('-topmost', 'true')

    # StrVars
    # drop_off_fee_StrVar = StringVar()

    Label(top, text="Please leave your Feedback:").pack(
        fill="both", expand=True)
    customer_feedback_box = Text(top)
    customer_feedback_box.pack(fill="both", expand=True)
    # Custom GetImagesWidget
    condition_photos_label = Label(
        top, text="Tool Condition Photos:").pack(fill="both", expand=True)
    images_widget = GetImagesWidget(
        top, empty_message='Add Photo', max_items=3)
    images_widget.pack(fill="both", expand=True)

    Button(
        top,
        text="Return to Owner",
        command=lambda: self.mark_as_returned_to_owner(
            Order_Dictionary, customer_feedback_box, images_widget, returnto='owner')
    ).pack(fill="both", expand=True)
    Button(
        top,
        text="Return to Depot",
        command=lambda: self.mark_as_returned_to_owner(
            Order_Dictionary, customer_feedback_box, images_widget, returnto='depot'),
    ).pack(fill="both", expand=True)
    Button(
        top,
        text="Request Pick-Up",
        command=lambda: self.mark_as_returned_to_owner(
            Order_Dictionary, customer_feedback_box, images_widget, returnto='depot', fee=True),
    ).pack(fill="both", expand=True)


def mark_as_returned_to_owner(self, Order_Dictionary, customer_feedback_box, images_widget, returnto, fee=False):
    self.order_instance.update_order(
        Unique_Order_ID=Order_Dictionary.get("Unique_Order_ID"),
        Customer_Feedback=customer_feedback_box.get(
            "1.0", 'end-1c').replace("'", "''"),
        Customer_Condition_Photos=self.get_image_paths_str_DB_ready(
            images_widget)
    )
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
    if fee == True:
        Tool_Dictionary = self.tool_instance.fetch_tool_by_tool_id(
            Order_Dictionary.get('Unique_Item_Number'))
        self.order_instance.update_order(
            Unique_Order_ID=Order_Dictionary.get('Unique_Order_ID'),
            Order_State='Complete',
            Drop_Off_Fee=Tool_Dictionary.get('Drop_Off_Fee')
        )
    else:
        self.order_instance.update_order(
            Unique_Order_ID=Order_Dictionary.get('Unique_Order_ID'),
            Order_State='Complete',
        )
    self.view_listed_orders_UI()


# Mark as received Here


def mark_as_received(self, Order_Dictionary):
    self.tool_instance.update_tool(
        Unique_Item_Number=Order_Dictionary.get('Unique_Item_Number'),
        Item_Process_State='with user'
    )
    self.order_instance.update_order(
        Unique_Order_ID=Order_Dictionary.get('Unique_Order_ID'),
        Order_State='Not_Complete',
    )
    self.view_listed_orders_UI()


def cancel_order(self, Order_Dictionary, Tool_Dictionary):
    answer = messagebox.askyesnocancel(
        "Delete Tool Listing",
        "Are you sure that you want to cancel this order?",
        icon='warning'
    )
    if answer == 1:
        process_state = Tool_Dictionary.get('Item_Process_State')
        orvar = False
        if process_state == 'with owner':
            orvar = True
        if process_state == 'with depot':
            orvar = True
        if orvar:
            self.order_instance.cancel_order(
                Order_Dictionary.get('Unique_Order_ID'))
        else:
            messagebox.showerror(
                title='Error', message='Tool must be with owner or at the depot')
    self.view_listed_orders_UI()
