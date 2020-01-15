from tkinter import Toplevel, Label
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.calendar_ import Calendar
    from Classes.tkinterwidgets.dateentry import DateEntry
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def view_bookings_Calendar_UI(self, ToolDictionary):
    top = Toplevel(self.root)
    top.attributes('-topmost', 'true')
    cal = Calendar(top, selectmode='none', day=40, date_pattern='d/m/yyyy')
    Tool_ID = ToolDictionary.get('Unique_Item_Number', '')
    OrdersList = self.order_instance.fetch_orders_from_tool_id(Tool_ID)
    bookined_dates = []
    for order in OrdersList:
        OrderDictionary = dict(
            zip(self.order_instance.orders_table_Index, order))
        if OrderDictionary.get('Order_State') != 'Complete':
            start_date = self.string_to_datetime(
                OrderDictionary.get('Booking_Start_Day')
            )
            if OrderDictionary.get('Order_Type') == 'Full Day':
                end_date = self.string_to_datetime(
                    OrderDictionary.get('Booking_End_Day')
                )
                for i in range(0, (end_date-start_date).days+1):
                    date = start_date + cal.timedelta(days=i)
                    cal.calevent_create(date, 'Booked', 'full_day')
            elif OrderDictionary.get('Order_Type') == 'Half Day':
                order_hours = OrderDictionary.get('Order_Hours')
                if order_hours == '6:00-12:00':
                    cal.calevent_create(
                        start_date, 'Booked', 'half_day_morning')
                elif order_hours == '12:00-18:00':
                    cal.calevent_create(
                        start_date, 'Booked', 'half_day_evening')
    cal.tag_config('full_day', background='red', foreground='yellow')
    cal.tag_config('half_day_morning', background='yellow', foreground='black')
    cal.tag_config('half_day_evening', background='green', foreground='black')
    cal.pack(fill="both", expand=True)
    Label(top, text='Half Day - 6:00-12:00',
          bg='yellow').pack(fill="both")
    Label(top, text='Half Day - 12:00-18:00',
          bg='green').pack(fill="both")
    Label(top, text='Full Day', bg='red').pack(fill="both")
