#Common Package
This is a common package for base, my web project base package.

+ Dto
  + ResObj (this is Response Dto format:{"code":200, "message":"", data: None})


+ handler
  + exception_handler (this is gobal exception handler)

+ Exception (this is custom exception)
  + AuthException
  + BusinessException

+ Utils 
  + date_util
    + get_time_by_str(date_str, date_format=DATE_TIME_FORMAT)
    + convert_date_str_format(date_str, old_format, new_format)
    + get_date_str_by_time(date_format, timestamp)
  + file_util
    + read_files_in_folder(file_path)
    + write_json_to_file(file_path, data, encoding='UTF-8')
  + http_util
    + get(url, params=None, headers=None)
    + get_json(url, params=None, headers=None)
    + post(url, params=None, headers=None, timeout=30)
    + post_json(url, params=None, headers=None, timeout=30)
  + festival_util
    + get_holiday_date_by_year_name(year, festival_name)
    + get_holiday_by_date(date_str)
    + is_holiday(date_str)