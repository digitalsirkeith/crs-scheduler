from dateutil.parser import parse
from datetime import time

def to_time(given_time):
    if type(given_time) is str:
        return parse(given_time).time()
    elif type(given_time) is time:
        return given_time
    else:
        return None

def to_str(day_of_week):
    if type(day_of_week) is str:
        return day_of_week
    return DayOfWeek.dlist[day_of_week]

def to_data(day_of_week):
    if type(day_of_week) is int:
        return day_of_week
    return DayOfWeek.dlist.index(day_of_week)

class DayOfWeek():
    dlist = ['M', 'T', 'W', 'Th', 'F', 'S']