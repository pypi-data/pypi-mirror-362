from datetime import datetime, timezone

def AgoraTimeStamp(tm=-1) -> float:
    if tm == -1:
        tm = datetime.utcnow()
    dt_utc = datetime(tm.year, tm.month, tm.day,
                      tm.hour, tm.minute, tm.second, tm.microsecond,
                      tzinfo=timezone.utc)
    delta = dt_utc.timestamp() - tm.timestamp()
    return (tm.timestamp() + delta) * 1000


def UTCDateTime(tm: float) -> datetime:
    dt = datetime.utcfromtimestamp(tm/1000).replace(tzinfo=timezone.utc)
    return dt
