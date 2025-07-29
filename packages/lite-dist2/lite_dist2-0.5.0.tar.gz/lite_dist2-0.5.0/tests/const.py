from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")
DT = datetime(2025, 4, 27, 20, 36, 10, 0, tzinfo=JST)
