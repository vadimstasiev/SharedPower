from tkinter import Toplevel
from Classes.tkinterwidgets.calendar_ import Calendar
from Classes.DatabaseInterfaceClass import DatabaseInterfaceClass


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

# OBSOLETE
# def pack_availability_dates_DB_READY(self, availability_list_pair):
#     pair_list = availability_list_pair
#     packed_availability_str = ""
#     for pair in pair_list:
#         for date in pair:
#             packed_availability_str += '#' + self.datetime_to_string(date)
#     packed_availability_str = packed_availability_str.replace(
#         "#", "", 1)  # Remove first "#"
#     return packed_availability_str


# OBSOLETE
# def unpack_dates_from_DB(self, __DB_packed_dates):
#     __list = __DB_packed_dates.split('#')
#     unpacked_dates = []
#     for i in __list:
#         unpacked_dates.append(i.strip('#'))
#     pair_list = []
#     for i in range(0, len(unpacked_dates)-1, 2):
#         start_date = unpacked_dates[i]
#         end_date = unpacked_dates[i+1]
#         pair_list.append((self.string_to_datetime(
#             start_date), self.string_to_datetime(end_date)))
#     # Returns a list with the dates paired e.g. [[start_date][end_date],[start_date][end_date], etc]
#     return pair_list
