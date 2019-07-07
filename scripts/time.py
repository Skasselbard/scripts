from datetime import datetime
from datetime import date

timeFormat = '%d.%m.%Y %H:%M:%S'


def toString(timestemp):
    return timestemp.strftime(timeFormat)


def fromString(string):
    return datetime.strptime(string, timeFormat)
