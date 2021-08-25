from datetime import datetime as dt

def datetime_format(datetime) -> str:
    return dt.strftime(datetime, "%Y-%m-%d %H:%M:%S")