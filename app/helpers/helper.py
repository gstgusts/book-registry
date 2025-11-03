from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import datetime, timezone


def date_to_bigint(date_str: str) -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return int(dt.timestamp() * 1000)


def date_to_unix_ms_local(date_str: str, tz_name: str = "Europe/Riga") -> int:
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=ZoneInfo(tz_name))
    return int(dt.timestamp() * 1000)


def date_to_unix_ms(date_str: str) -> int:
    # Interpret the date as midnight *UTC* on that calendar day
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)
