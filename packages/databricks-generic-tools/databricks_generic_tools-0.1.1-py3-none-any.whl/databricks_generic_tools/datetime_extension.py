from datetime import datetime, timezone

__all__ = ["utcRunDatetime", "mscurrentday"]

def utcRunDatetime() -> str:    
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds')

def mscurrentday() -> int:
    _now: datetime = datetime.now(timezone.utc)
    return int((_now.hour * 3600 + _now.minute * 60 + _now.second) * 1000 + _now.microsecond // 1000)