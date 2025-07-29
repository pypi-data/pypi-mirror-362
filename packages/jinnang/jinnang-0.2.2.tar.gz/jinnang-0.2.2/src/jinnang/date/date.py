from datetime import datetime
from typing import Optional

import pytz
from dateutil import parser

def date_str_to_iso_date_str(date_str: Optional[str], target_timezone: str = 'Asia/Shanghai') -> Optional[str]:
    if not date_str:
        return None
    try:
        if ' ' in date_str:
            parts = date_str.split(' ')
            if len(parts) > 0 and parts[0].count(':') > 0:
                parts[0] = parts[0].replace(':', '-', 2)
                date_str = ' '.join(parts)
        dt = parser.parse(date_str)
        if dt.microsecond:
            dt = dt.replace(microsecond=0)
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        target_tz = pytz.timezone(target_timezone)
        localized = dt.astimezone(target_tz)
        return localized.isoformat(timespec='seconds')
    except Exception:
        return None

def timestamp_to_date(timestamp, fstr='%y%m%d', timezone='Asia/Shanghai'):
    utc_dt = datetime.utcfromtimestamp(timestamp)
    utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
    my_tz = pytz.timezone(timezone)
    my_dt = utc_dt.astimezone(my_tz)
    return my_dt.strftime(fstr)