import holidays

from src.constants.festival import FESTIVAL_DAY


def get_holiday_date_by_year_name(year, festival_name):
    """
    Obtain the holiday(China) date of the current year based on the year and holiday name
    根据年份以及节日名获取当年的节日日期
    :param year:
    :param festival_name: reference constants/festival
    :return: date
    """
    cn_holidays = holidays.CN(language='zh_CN', years=int(year))
    for date, name in cn_holidays.items():
        if name == FESTIVAL_DAY.get(festival_name):
            return date


def get_holiday_by_date(date_str):
    """
    get holiday name by date
    根据日期获取节假日名
    :param date_str: date str
    :return: holiday name
    """
    year = date_str.split('-')[0]
    cn_holidays = holidays.CN(language='zh_CN', years=int(year))
    for date, name in cn_holidays.items():
        if str(date) == date_str:
            return name


def is_holiday(date_str):
    """
    check the date is holiday or not
    :param date_str: date str
    :return:
    """
    year = date_str.split('-')[0]
    cn_holidays = holidays.CN(language='zh_CN', years=int(year))
    return date_str in cn_holidays
