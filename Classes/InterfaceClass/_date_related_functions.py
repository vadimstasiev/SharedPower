from tkinter import Toplevel
try:  # Otherwise pylint complains
    from Classes.tkinterwidgets.calendar_ import Calendar
    from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass
except:
    pass


def view_bookings_Calendar_UI(self, availability_Pair_dict):
    booked_dates = list(tuple(availability_Pair_dict))
    startday, _ = booked_dates.pop(0)
    top = Toplevel(self.root)
    cal = Calendar(top, selectmode='none', date_pattern='d/m/yyyy',
                   day=startday.day, month=startday.month, year=startday.year)
    # mindate and maxdate from Calendar are broken, DO NOT USE
    for dates in booked_dates:
        start_date, end_date = dates
        for i in range(0, (end_date-start_date).days+1):
            date = start_date + cal.timedelta(days=i)
            cal.calevent_create(date, 'Booked', 'booked')
    cal.tag_config('booked', background='red', foreground='yellow')
    cal.pack(fill="both", expand=True)
