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
from functools import total_ordering
from math import floor

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
@total_ordering
class GregorianCalendar:
    def __init__(self, year, month, day):
        if (
            not isinstance(year, int)
            or not isinstance(month, int)
            or not isinstance(day, int)
        ):
            raise TypeError("integer argument expected")
        if month < 1 or month > 12:
            raise ValueError(
                "Month must be between 1 and 12, while it is {}.".format(month)
            )
        if (
            day < 1
            or day > _days_in_month[GregorianCalendar.is_leap_year(year)][month - 1]
        ):
            raise ValueError(
                "Day must be between 1 and number of days in month, while it is {}.".format(
                    day
                )
            )
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
            raise ValueError(
                "Day must be between 1 and number of days in year, while it is {}.".format(
                    day
                )
            )
        month = bisect.bisect_left(
            _days_in_previous_months[GregorianCalendar.is_leap_year(year)], day
        )
        day_in_month = (
            day
            - _days_in_previous_months[GregorianCalendar.is_leap_year(year)][month - 1]
        )
        return cls(year, month, day_in_month)

    @classmethod
    def from_rata_die(cls, day_count):
        if not isinstance(day_count, int):
            raise TypeError("integer argument expected")
        y400, d400 = divmod(day_count - 1, 146097)
        y100, d100 = divmod(d400, 36524)
        y4, d4 = divmod(d100, 1461)
        y1 = d4 // 365
        year_minus_one = (
            400 * y400 + 100 * y100 + 4 * y4 + y1 - (1 if (y100 == 4 or y1 == 4) else 0)
        )
        days = (
            day_count
            - 365 * year_minus_one
            - year_minus_one // 4
            + year_minus_one // 100
            - year_minus_one // 400
        )  # days from january 1st (included) to today
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
            self._rata_die = (
                365 * (self._year - 1)
                + (self._year - 1) // 4
                - (self._year - 1) // 100
                + (self._year - 1) // 400
                + (367 * self._month - 362) // 12
                + (
                    (-1 if GregorianCalendar.is_leap_year(self._year) else -2)
                    if self._month > 2
                    else 0
                )
                + self._day
            )
        return self._rata_die

    def weekday(self):
        return (self.to_rata_die() - 1) % 7 + 1

    def day_of_year(self):
        return self.to_rata_die() - (
            365 * (self._year - 1)
            + (self._year - 1) // 4
            - (self._year - 1) // 100
            + (self._year - 1) // 400
        )

    def replace(self, *, year=None, month=None, day=None):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        return self.__class__(year, month, day)

    # Comparison operators
    def __eq__(self, other):
        return (
            isinstance(other, GregorianCalendar)
            and self.year == other.year
            and self.month == other.month
            and self.day == other.day
        )

    def __gt__(self, other):
        if isinstance(other, GregorianCalendar):
            return (self.year, self.month, self.day) > (
                other.year,
                other.month,
                other.day,
            )
        else:
            return NotImplemented

    # hash value
    def __hash__(self):
        return hash((self.year, self.month, self.day))

    def __repr__(self):
        return "datetime2.western.{}({}, {}, {})".format(
            self.__class__.__name__, self.year, self.month, self.day
        )

    def __str__(self):
        if self.year >= 0:
            return "{:04d}-{:02d}-{:02d}".format(self.year, self.month, self.day)
        else:
            return "{:05d}-{:02d}-{:02d}".format(self.year, self.month, self.day)

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
        "d": lambda self: "{:02d}".format(self.day),
        "m": lambda self: "{:02d}".format(self.month),
        "j": lambda self: "{:03d}".format(self.day_of_year()),
        "U": lambda self: "{:02d}".format(
            (self.day_of_year() + (13 - self.weekday()) % 7) // 7
        ),
        "w": lambda self: "{:1d}".format(self.weekday()),
        "W": lambda self: "{:02d}".format(
            (self.day_of_year() + 7 - self.weekday()) // 7
        ),
        "y": lambda self: "{:03d}".format(self.year)[-2:],
        "Y": lambda self: "{:04d}".format(self.year)
        if self.year >= 0
        else "-{:04d}".format(-self.year),
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
    def __init__(self, hour, minute, second, *, to_utc=None):
        if not isinstance(hour, int) or not isinstance(minute, int):
            raise TypeError("Hour and minute must be integer")
        if hour < 0 or hour > 23:
            raise ValueError(
                "Hour must be between 0 and 23, while it is {}.".format(hour)
            )
        if minute < 0 or minute > 59:
            raise ValueError(
                "Minute must be between 0 and 59, while it is {}.".format(minute)
            )
        try:
            second_fraction = verify_fractional_value(second, min=0, max_excl=60)
        except TypeError as exc:
            raise TypeError("Second is not a valid fractional value") from exc
        except ValueError as exc:
            raise ValueError(
                "Second must be equal or greater than 0 and less than 60."
            ) from exc
        self._hour = hour
        self._minute = minute
        self._second = second_fraction
        self._day_frac = None
        if to_utc is None:
            self._to_utc = None
        else:
            try:
                candidate_to_utc = verify_fractional_value(to_utc, min=-24, max=+24)
            except TypeError as exc:
                raise TypeError("Time zone is not a valid fractional value") from exc
            except ValueError as exc:
                raise ValueError(
                    "Time zone must be greater than -24 and less than 24."
                ) from exc
            self._to_utc = candidate_to_utc

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
    def to_utc(self):
        return self._to_utc

    @classmethod
    def from_day_frac(cls, day_frac):
        if not isinstance(day_frac, Fraction):
            raise TypeError("Fraction argument expected")
        if day_frac < 0 or day_frac >= 1:
            raise ValueError(
                "Day fraction must be equal or greater than 0 and less than 1, while it is {}.".format(
                    day_frac
                )
            )
        hour = int(day_frac * 24)
        minute = int((day_frac - Fraction(hour, 24)) * 1440)
        second = (day_frac - Fraction(hour, 24) - Fraction(minute, 1440)) * 86400
        western = cls(hour, minute, second)
        western._day_frac = day_frac
        return western

# todo: Fix from_time_pair and to_time_pair
    @classmethod
    def from_time_pair(cls, day_frac, to_utc):
        ###################### DUMMY METHOD, WILL NEVER WORK AS IS ######################
        if not isinstance(day_frac, Fraction):
            raise TypeError("Fraction argument expected for day fraction")
        if not isinstance(to_utc, Fraction):
            raise TypeError("Fraction argument expected for fraction to UTC")
        if day_frac < 0 or day_frac >= 1:
            raise ValueError("Day fraction must be equal or greater than 0 and less than 1, while it is {}.".format(day_frac))
        if to_utc < -1 or to_utc > 1:
            raise ValueError("Fraction to UTC must be greater or equal to -1 and less or equal to 1, while it is {}.".format(day_frac))
        utc_time = day_frac - to_utc
        utc_time_normalized = utc_time - floor(utc_time) # we keep only the fraction
        hour = int(utc_time_normalized * 24)
        minute = int((utc_time_normalized - Fraction(hour, 24)) * 1440)
        second = (utc_time_normalized - Fraction(hour, 24) - Fraction(minute, 1440)) * 86400
        western = cls(hour, minute, second)
        western._day_frac = day_frac
        return western

    def to_time_pair(self):
        ###################### DUMMY METHOD, WILL NEVER WORK AS IS ######################
        return self._beat / 1000, Fraction(-1, 24)


    def to_day_frac(self):
        if self._day_frac is None:
            self._day_frac = (
                self._second / 86400
                + Fraction(self.minute, 1440)
                + Fraction(self.hour, 24)
            )
        return self._day_frac

    def replace(self, *, hour=None, minute=None, second=None):
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        return self.__class__(hour, minute, second)

    def __repr__(self):
        return "datetime2.western.{}({}, {}, {})".format(
            self.__class__.__name__, self.hour, self.minute, repr(self.second)
        )

    def __str__(self):
        return "{:02d}:{:02d}:{:02d}".format(self.hour, self.minute, int(self.second))

    format_functions = {
        "H": lambda self: "{:02d}".format(self.hour),
        "I": lambda self: "{:02d}".format(
            12 if self.hour == 0 else self.hour if self.hour <= 12 else self.hour - 12
        ),
        "p": lambda self: "AM" if self.hour < 12 else "PM",
        "M": lambda self: "{:02d}".format(self.minute),
        "S": lambda self: "{:02d}".format(floor(self.second)),
        "f": lambda self: "{:06d}".format(
            int((self.second - floor(self.second)) * 1000000)
        ),
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
