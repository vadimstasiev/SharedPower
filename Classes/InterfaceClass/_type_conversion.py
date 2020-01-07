import datetime
from Classes.MoneyParser import price_str, price_dec


def get_savable_int_price(self, __price):
    return int(float(price_str(__price))*100)


def get_displayable_price(self, __price):
    return "£ "+str(price_dec(str(float(__price)/100)))


def datetime_to_string(self, _datetime: datetime.datetime):
    return _datetime.strftime('%d/%m/%Y')


def string_to_datetime(self, _string: str):
    return datetime.datetime.strptime(_string, '%d/%m/%Y')
