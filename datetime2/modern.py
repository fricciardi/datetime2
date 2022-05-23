# ISO calendar and Internet time

# Copyright (c) 2013-2022 Francesco Ricciardi
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


__all__ = ["IsoCalendar"]


import bisect
from fractions import Fraction
from math import floor

from datetime2 import verify_fractional_value

_long_years = frozenset(
    [
        4,
        9,
        15,
        20,
        26,
        32,
        37,
        43,
        48,
        54,
        60,
        65,
        71,
        76,
        82,
        88,
        93,
        99,
        105,
        111,
        116,
        122,
        128,
        133,
        139,
        144,
        150,
        156,
        161,
        167,
        172,
        178,
        184,
        189,
        195,
        201,
        207,
        212,
        218,
        224,
        229,
        235,
        240,
        246,
        252,
        257,
        263,
        268,
        274,
        280,
        285,
        291,
        296,
        303,
        308,
        314,
        320,
        325,
        331,
        336,
        342,
        348,
        353,
        359,
        364,
        370,
        376,
        381,
        387,
        392,
        398,
    ]
)

_weeks_in_previous_years = [0]
for year_index in range(1, 400):
    _weeks_in_previous_years.append(_weeks_in_previous_years[-1] + (52 if year_index not in _long_years else 53))


# This code pretty prints the week-in-previous-years list
# for row in range (20):
#    print('{:3d}: {}'.format(row * 20, " ".join(['{:5d}'.format(_weeks_in_previous_years[y + row * 20]) for y in range(20)])))


##############################################################################
# Iso calendar
#
class IsoCalendar:
    def __init__(self, year, week, day):
        if not isinstance(year, int) or not isinstance(week, int) or not isinstance(day, int):
            raise TypeError("integer argument expected")
        if week < 1 or week > IsoCalendar.weeks_in_year(year):
            raise ValueError(f"Week must be between 1 and number of weeks in year, while it is {week}.")
        if day < 1 or day > 7:
            raise ValueError(f"Day must be between 1 and 7, while it is {day}.")
        self._year = year
        self._week = week
        self._day = day
        self._rata_die = None

    @property
    def year(self):
        return self._year

    @property
    def week(self):
        return self._week

    @property
    def day(self):
        return self._day

    @classmethod
    def from_rata_die(cls, day_count):
        if not isinstance(day_count, int):
            raise TypeError("integer argument expected")
        week_no_less_1, day_less_1 = divmod(day_count - 1, 7)  # ranges: week_no_less_1: free, day_less_1: 0..6
        four_hundred_years, no_of_weeks_in_400 = divmod(week_no_less_1, 20871)  # ranges: four_hundred_years: free, no_of_weeks_in_400: 0..20870
        year_in_400 = bisect.bisect_right(_weeks_in_previous_years, no_of_weeks_in_400)  # range: year_in_400: 1..400
        year = year_in_400 + four_hundred_years * 400
        week = no_of_weeks_in_400 - _weeks_in_previous_years[year_in_400 - 1] + 1
        day = day_less_1 + 1
        iso_day = cls(year, week, day)
        iso_day._rata_die = day_count
        return iso_day

    @staticmethod
    def is_long_year(year):
        return year % 400 in _long_years

    @staticmethod
    def weeks_in_year(year):
        return 52 if year % 400 not in _long_years else 53

    def to_rata_die(self):
        if self._rata_die is None:
            y400, year_in_400 = divmod(self.year - 1, 400)
            self._rata_die = (y400 * 146097 + 7 * (_weeks_in_previous_years[year_in_400] + self.week - 1) + self.day)
        return self._rata_die

    def day_of_year(self):
        return 7 * (self.week - 1) + self.day

    def replace(self, *, year=None, week=None, day=None):
        if year is None:
            year = self.year
        if week is None:
            week = self.week
        if day is None:
            day = self.day
        return type(self)(year, week, day)

    def __repr__(self):
        return f"datetime2.modern.{type(self).__name__}({self.year}, {self.week}, {self.day})"

    def __str__(self):
        if self.year >= 0:
            return f"{self.year:04d}-W{self.week:02d}-{self.day:1d}"
        else:
            return f"{self.year:05d}-W{self.week:02d}-{self.day:1d}"

    name_weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    format_functions = {
        "a": lambda self: IsoCalendar.name_weekdays[self.day - 1][:3],
        "A": lambda self: IsoCalendar.name_weekdays[self.day - 1],
        "j": lambda self: f"{self.day_of_year():03d}",
        "w": lambda self: f"{self.day:1d}",
        "W": lambda self: f"{(self.day_of_year() + 7 - self.day) // 7:02d}",
        "y": lambda self: f"{self.year:03d}"[-2:],
        "Y": lambda self: f"{self.year:04d}" if self.year >= 0 else f"-{-self.year:04d}"
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
# Internet time representation
#
class InternetTime:
    def __init__(self, beat):
        try:
            beat_fraction = verify_fractional_value(beat, min=0, max_excl=1000)
        except TypeError as exc:
            raise TypeError("beat is not a valid fractional value") from exc
        except ValueError as exc:
            raise ValueError("beat must be equal or greater than 0 and less than 1000.") from exc
        self._beat = beat_fraction

    @property
    def beat(self):
        return self._beat

    @classmethod
    def from_time_pair(cls, day_frac, utcoffset):
        day_frac_valid = verify_fractional_value(day_frac, min=0, max_excl=1, strict=True)
        if utcoffset is None:
            raise TypeError("Internet time can only be used for aware Time instances.")
        utcoffset_valid = verify_fractional_value(utcoffset, min=-1, max=1, strict=True)
        utc_time = day_frac_valid - utcoffset_valid
        beat = (utc_time - floor(utc_time)) * 1000
        internet = cls(beat)
        return internet

    def to_time_pair(self):
        return self._beat / 1000, Fraction(-1, 24)

    def __repr__(self):
        return f"datetime2.modern.{type(self).__name__}({self.beat!r})"

    def __str__(self):
        return f"@{int(self.beat):03d}"

    format_functions = {
        "b": lambda self: f"{int(self.beat):03d}",
        "f": lambda self: f"{int((self.beat - int(self.beat)) * 1000):03d}"
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
