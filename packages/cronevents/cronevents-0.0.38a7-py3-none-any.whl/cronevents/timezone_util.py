import zoneinfo
import warnings
from dataclasses import dataclass


@dataclass
class TimezoneAbbr:
    tz: str
    abbr: str


class TimezoneConverter:
    converts: list[TimezoneAbbr]

    def __init__(self):
        self.converts = []

    def add(self, tz, abbr):
        if not self.valid_tz(tz):
            raise ValueError(f'Invalid timezone: {tz}. See valid timezone by calling `zoneinfo.available_timezones()`')

        if abbr in self:
            warnings.warn(f'Abbreviation \'{abbr}\' already exists, added it again will do nothing. Value: {self[abbr]}')

        self.converts.append(TimezoneAbbr(tz, abbr))

    def get_abbrs(self, tz) -> list[str]:
        if not self.valid_tz(tz):
            raise ValueError(f'Invalid timezone: {tz}. See valid timezone by calling `zoneinfo.available_timezones()`')

        abbrs = []
        for tz_abbr in self.converts:
            if tz_abbr.tz == tz:
                abbrs.append(tz_abbr.abbr)
        return abbrs

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, item):
        for tz_abbr in self.converts:
            if tz_abbr.tz == item or tz_abbr.abbr == item:
                return tz_abbr
        return None

    def __contains__(self, item):
        for tz_abbr in self.converts:
            if tz_abbr.tz == item or tz_abbr.abbr == item:
                return True
        return False

    @staticmethod
    def valid_tz(tz: str) -> bool:
        return tz in zoneinfo.available_timezones()

    def is_timezone(self, tz: str) -> bool:
        if tz in self:
            return True
        return self.valid_tz(tz)

    def tz_to_timezone(self, tz: str):
        if self.valid_tz(tz):
            return zoneinfo.ZoneInfo(tz)

        if tz in self:
            return zoneinfo.ZoneInfo(self[tz].tz)

        raise ValueError(f'Invalid timezone: {tz}')


