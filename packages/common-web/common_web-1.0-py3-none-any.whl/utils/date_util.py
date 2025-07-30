"""
date time util
"""
import time

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATE_TIME_FORMAT = "%y-%m-%d %H:%M:%S"
DATE_JOIN_FORMAT = "%y%m%d"
DATE_TIME_JOIN_FORMAT = "%y%m%d%H%M%S"

def get_time_by_str(date_str, date_format=DATE_TIME_FORMAT):
    """get timestamp by date str, if date format is None, default format: %y-%M-%D %H:%M:%S"""
    t = time.strptime(date_str, date_format)
    return time.mktime(t)


def convert_date_str_format(date_str, old_format, new_format):
    """convet date str from old format to new format"""
    t = time.strptime(date_str, old_format)
    return time.strftime(new_format, t)


def get_date_str_by_time(date_format, timestamp):
    """get date str by timestamp"""
    t = time.localtime(timestamp)
    return time.strftime(date_format, t)
