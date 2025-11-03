# app/models/types.py
from datetime import date, datetime, time, timezone
from sqlalchemy.types import TypeDecorator, BigInteger


class EpochMsDate(TypeDecorator):
    impl = BigInteger
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, date) and not isinstance(value, datetime):
            dt = datetime.combine(value, time(0, 0), tzinfo=timezone.utc)
        elif isinstance(value, datetime):
            dt = value.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return int(value)
        return int(dt.timestamp() * 1000)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).date()