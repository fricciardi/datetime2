# Gregorian calendar in calendars package

# Copyright (c) 2012-2022 Francesco Ricciardi
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name(s) of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AS IS AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__author__ = "Francesco Ricciardi <francescor2010 at yahoo.it>"


import bisect
from fractions import Fraction

from .common import verify_fractional_value


_days_in_month = [
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
]

_days_in_previous_months = [
    [sum(_days_in_month[leap_year][:month]) for month in range(12)]
    for leap_year in (0, 1)
]


##############################################################################
# Gregorian calendar
#
class GregorianCalendar:
    def __init__(self, year, month, day):
        if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
            raise TypeError("integer argument expected")
        if month < 1 or month > 12:
            raise ValueError(f"Month must be between 1 and 12, while it is {month}.")
        if day < 1 or day > _days_in_month[GregorianCalendar.is_leap_year(year)][month - 1]:
            raise ValueError(f"Day must be between 1 and number of days in month, while it is {day}.")
        self._year = year
        self._month = month
        self._day = day
        self._rata_die = None

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @classmethod
    def year_day(cls, year, day):
        if not isinstance(year, int) or not isinstance(day, int):
            raise TypeError("integer argument expected")
        if day < 1 or day > (366 if GregorianCalendar.is_leap_year(year) else 365):
            raise ValueError(f"Day must be between 1 and number of days in year, while it is {day}.")
        month = bisect.bisect_left(_days_in_previous_months[GregorianCalendar.is_leap_year(year)], day)
        day_in_month = (day - _days_in_previous_months[GregorianCalendar.is_leap_year(year)][month - 1])
        return cls(year, month, day_in_month)

    @classmethod
    def from_rata_die(cls, day_count):
        if not isinstance(day_count, int):
            raise TypeError("integer argument expected")
        y400, d400 = divmod(day_count - 1, 146097)
        y100, d100 = divmod(d400, 36524)
        y4, d4 = divmod(d100, 1461)
        y1 = d4 // 365
        year_minus_one = (400 * y400 + 100 * y100 + 4 * y4 + y1 - (1 if (y100 == 4 or y1 == 4) else 0))
        days = (day_count - 365 * year_minus_one - year_minus_one // 4 + year_minus_one // 100 - year_minus_one // 400)  # days from january 1st (included) to today
        greg_day = cls.year_day(year_minus_one + 1, days)
        greg_day._rata_die = day_count
        return greg_day

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0) and (year % 400 not in (100, 200, 300))

    @staticmethod
    def days_in_year(year):
        return 365 if not GregorianCalendar.is_leap_year(year) else 366

    def to_rata_die(self):
        if self._rata_die is None:
            self._rata_die = (365 * (self._year - 1)
                + (self._year - 1) // 4
                - (self._year - 1) // 100
                + (self._year - 1) // 400
                + (367 * self._month - 362) // 12
                + ((-1 if GregorianCalendar.is_leap_year(self._year) else -2) if self._month > 2 else 0)
                + self._day)
        return self._rata_die

    def weekday(self):
        return (self.to_rata_die() - 1) % 7 + 1

    def day_of_year(self):
        return self.to_rata_die() - (365 * (self._year - 1) + (self._year - 1) // 4
                                     - (self._year - 1) // 100 + (self._year - 1) // 400)

    def replace(self, *, year=None, month=None, day=None):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        return type(self)(year, month, day)

    def __repr__(self):
        return f"datetime2.western.{type(self).__name__}({self.year}, {self.month}, {self.day})"

    def __str__(self):
        if self.year >= 0:
            return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"
        else:
            return f"{self.year:05d}-{self.month:02d}-{self.day:02d}"

    name_weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    name_months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    format_functions = {
        "a": lambda self: GregorianCalendar.name_weekdays[self.weekday() - 1][:3],
        "A": lambda self: GregorianCalendar.name_weekdays[self.weekday() - 1],
        "b": lambda self: GregorianCalendar.name_months[self.month - 1][:3],
        "B": lambda self: GregorianCalendar.name_months[self.month - 1],
        "d": lambda self: f"{self.day:02d}",
        "m": lambda self: f"{self.month:02d}",
        "j": lambda self: f"{self.day_of_year():03d}",
        "U": lambda self: f"{(self.day_of_year() + (13 - self.weekday()) % 7) // 7:02d}",
        "w": lambda self: f"{self.weekday():1d}",
        "W": lambda self: f"{(self.day_of_year() + 7 - self.weekday()) // 7:02d}",
        "y": lambda self: f"{self.year:03d}"[-2:],
        "Y": lambda self: f"{self.year:04d}" if self.year >= 0 else f"-{-self.year:04d}",
    }

    def cformat(self, format_string):
        if not isinstance(format_string, str):
            raise TypeError("Format must be specified with string.")
        output_pieces = []
        for format_chunk in format_string.split("%%"):
            format_parts = format_chunk.split("%")
            chunk_pieces = [format_parts[0]]
            for part in format_parts[1:]:
                if part == "":  # special case: last char is '%'
                    value = "%"
                else:
                    try:
                        value = self.format_functions[part[0]](self)
                    except KeyError:
                        value = "%" + part[0]
                chunk_pieces.append(value)
                chunk_pieces.append(part[1:])
            output_pieces.append("".join(chunk_pieces))
        return "%".join(output_pieces)


##############################################################################
# Western time representation
class WesternTime:
    def __init__(self, hour, minute, second, *, timezone=None):
        if not isinstance(hour, int) or not isinstance(minute, int):
            raise TypeError("Hour and minute must be integer")
        if hour < 0 or hour > 23:
            raise ValueError(f"Hour must be between 0 and 23, while it is {hour}.")
        if minute < 0 or minute > 59:
            raise ValueError(f"Minute must be between 0 and 59, while it is {minute}.")
        try:
            second_fraction = verify_fractional_value(second, min=0, max_excl=60)
        except TypeError as exc:
            raise TypeError("Second is not a valid fractional value") from exc
        except ValueError as exc:
            raise ValueError("Second must be equal or greater than 0 and less than 60.") from exc
        self._hour = hour
        self._minute = minute
        self._second = second_fraction
        if timezone is None:
            self._timezone = None
        else:
            try:
                candidate_timezone = verify_fractional_value(timezone, min=-24, max=+24)
            except TypeError as exc:
                raise TypeError("Time zone is not a valid fractional value") from exc
            except ValueError as exc:
                raise ValueError("Time zone must be greater than -24 and less than 24.") from exc
            self._timezone = candidate_timezone

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def timezone(self):
        return self._timezone

    @classmethod
    def from_time_pair(cls, day_frac, utcoffset):
        day_frac_valid = verify_fractional_value(day_frac, min=0, max_excl=1, strict=True)
        hour = int(day_frac_valid * 24)
        minute = int((day_frac_valid - Fraction(hour, 24)) * 1440)
        second = (day_frac_valid - Fraction(hour, 24) - Fraction(minute, 1440)) * 86400
        if utcoffset is None:
            western = cls(hour, minute, second)
            return western
        else:
            utcoffset_valid = verify_fractional_value(utcoffset, min=-1, max=1, strict=True)
            western = cls(hour, minute, second, timezone=utcoffset_valid * 24)
            return western

    def to_time_pair(self):
        day_frac = self._second / 86400 + Fraction(self._minute, 1440) + Fraction(self._hour, 24)
        if self._timezone is None:
            return day_frac, None
        else:
            return day_frac, self._timezone / 24

    def replace(self, *, hour=None, minute=None, second=None, timezone=None):
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if timezone is None:
            return type(self)(hour, minute, second, timezone=self.timezone)
        else:
            if self.timezone is None:
                raise TypeError("Can replace timezone only in aware instances.")
            else:
                return type(self)(hour, minute, second, timezone=timezone)

    def __repr__(self):
        if self.timezone is None:
            return f"datetime2.western.{type(self).__name__}({self.hour}, {self.minute}, {self.second!r})"
        else:
            return f"datetime2.western.{type(self).__name__}({self.hour}, {self.minute}, {self.second!r}, timezone={self.timezone!r})"

    def __str__(self):
        time_str = f"{self.hour:02d}:{self.minute:02d}:{int(self.second):02d}"
        if self.timezone is None:
            return time_str
        else:
            tz_hour = int(self.timezone)
            hour_rest = (self.timezone - tz_hour) * 60
            tz_minute = int(hour_rest)
            return f"{time_str}{tz_hour:+02d}:{tz_minute:02d}"

    format_functions = {
        "H": lambda self: f"{self.hour:02d}",
        "I": lambda self: f"{12 if self.hour == 0 else self.hour if self.hour <= 12 else self.hour - 12:02d}",
        "p": lambda self: "AM" if self.hour < 12 else "PM",
        "M": lambda self: f"{self.minute:02d}",
        "S": lambda self: f"{int(self.second):02d}",
        "f": lambda self: f"{int((self.second - int(self.second)) * 1000000):06d}",
    }

    def cformat(self, format_string):
        if not isinstance(format_string, str):
            raise TypeError("Format must be specified with string.")
        output_pieces = []
        for format_chunk in format_string.split("%%"):
            format_parts = format_chunk.split("%")
            chunk_pieces = [format_parts[0]]
            for part in format_parts[1:]:
                if part == "":  # special case: last char is '%'
                    value = "%"
                elif part == 'z':  # this case is too complex to fit in a lambda
                    if self.timezone is None:
                        value = ''
                    else:
                        if self.timezone < 0:
                            tz_sign = '-'
                            abs_timezone = -self.timezone
                        else:
                            tz_sign = '+'
                            abs_timezone = self.timezone
                        tz_hour = int(abs_timezone)
                        remainder_in_minutes = (abs_timezone - tz_hour) * 60
                        tz_minute = int(remainder_in_minutes)
                        remainder_in_seconds = (remainder_in_minutes - tz_minute) * 60
                        tz_second = int(remainder_in_seconds)
                        remainder_in_microseconds = (remainder_in_seconds - tz_second) * 1_000_000
                        tz_microsecond = int(remainder_in_microseconds)
                        if tz_microsecond > 0:
                            value = f"{tz_sign}{tz_hour:02d}:{tz_minute:02d}:{tz_second:02d}.{tz_microsecond:06d}"
                        elif tz_second > 0:
                            value = f"{tz_sign}{tz_hour:02d}:{tz_minute:02d}:{tz_second:02d}"
                        else:
                            value = f"{tz_sign}{tz_hour:02d}:{tz_minute:02d}"
                else:
                    try:
                        value = self.format_functions[part[0]](self)
                    except KeyError:
                        value = "%" + part[0]
                chunk_pieces.append(value)
                chunk_pieces.append(part[1:])
            output_pieces.append("".join(chunk_pieces))
        return "%".join(output_pieces)
