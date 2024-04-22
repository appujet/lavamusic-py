import datetime
from typing import Optional, Sequence


class FormatUtils:
    @staticmethod
    def duration(milliseconds: int) -> str:
        units = [
            {"label": "year", "mod": 31536000000},
            {"label": "month", "mod": 2592000000},
            {"label": "week", "mod": 604800000},
            {"label": "day", "mod": 86400000},
            {"label": "hour", "mod": 3600000},
            {"label": "minute", "mod": 60000},
            {"label": "second", "mod": 1000},
        ]
        duration = milliseconds
        result = []
        for unit in units:
            label, mod = unit["label"], unit["mod"]
            if duration >= mod:
                val = int(duration / mod)
                duration = duration % mod
                result.append(f"{val} {label + 's' if val != 1 else label}")
        return ", ".join(result)

    @staticmethod
    def file_size(bytes_: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = bytes_
        unit = 0
        while size >= 1024:
            size /= 1024
            unit += 1
        return f"{size:.2f} {units[unit]}"

    @staticmethod
    def format_number(num: int) -> str:
        suffixes = ["", "K", "M", "B", "T"]
        magnitude = num // 3
        if magnitude == 0:
            return str(num)
        short_num = num / (10 ** (magnitude * 3))
        rounded_num = round(short_num, 1)
        suffix = suffixes[magnitude]
        return f"{rounded_num}{suffix}"

    @staticmethod
    def format_time(time: any) -> str:
        hours = time // 3600000
        minutes = (time % 3600000) // 60000
        seconds = ((time % 360000) % 60000) // 1000
        hours_string = str(hours).zfill(2)
        minutes_string = str(minutes).zfill(2)
        seconds_string = str(seconds).zfill(2)
        if hours >= 24:
            return "LIVE"
        elif hours > 0:
            return f"{hours_string}:{minutes_string}:{seconds_string}"
        else:
            return f"{minutes_string}:{seconds_string}"

    @staticmethod
    def string_to_ms(string: str) -> int:
        string = string.lower()
        string = string.replace(" ", "")
        string = string.replace("and", "")
        string = string.replace("a", "")
        string = string.replace("an", "")
        string = string.replace("years", "y")
        string = string.replace("year", "y")
        string = string.replace("months", "mo")
        string = string.replace("month", "mo")
        string = string.replace("weeks", "w")
        string = string.replace("week", "w")
        string = string.replace("days", "d")
        string = string.replace("day", "d")
        string = string.replace("hours", "h")
        string = string.replace("hour", "h")
        string = string.replace("minutes", "m")
        string = string.replace("minute", "m")
        string = string.replace("seconds", "s")
        string = string.replace("second", "s")
        string = string.replace(":", "")
        string = string.strip()
        string = string.split(" ")

        ms = 0
        for i in string:
            if i.endswith("y"):
                ms += int(i[:-1]) * 31536000000
            elif i.endswith("mo"):
                ms += int(i[:-2]) * 2592000000
            elif i.endswith("w"):
                ms += int(i[:-1]) * 604800000
            elif i.endswith("d"):
                ms += int(i[:-1]) * 86400000
            elif i.endswith("h"):
                ms += int(i[:-1]) * 3600000
            elif i.endswith("m"):
                ms += int(i[:-1]) * 60000
            elif i.endswith("s"):
                ms += int(i[:-1]) * 1000
            else:
                ms += int(i) * 1000
        return ms


def human_join(seq: Sequence[str], delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


def format_dt(dt: datetime.datetime, style: Optional[str] = None) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)

    if style is None:
        return f"<t:{int(dt.timestamp())}>"
    return f"<t:{int(dt.timestamp())}:{style}>"


class plural:
    def __init__(self, value: int):
        self.value: int = value

    def __format__(self, format_spec: str) -> str:
        v = self.value
        singular, sep, plural = format_spec.partition("|")
        plural = plural or f"{singular}s"
        if abs(v) != 1:
            return f"{v} {plural}"
        return f"{v} {singular}"
