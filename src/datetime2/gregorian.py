# datetime2 package main file

# Copyright (c) 2011 Francesco Ricciardi
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

__author__ = 'Francesco Ricciardi <francescor2010 at yahoo.it>'


__all__ = ['GregorianCalendar']


import bisect


_days_in_month = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                  [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

_days_in_previous_months = [ [ sum(_days_in_month[leap_year][:month]) for month in range(12)] for leap_year in (0, 1)]

##############################################################################
# Gregorian calendar
#
class GregorianCalendar:
    def __init__(self, year, month, day):
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12, while it is {}.".format(month))
        if day < 1 or day > _days_in_month[GregorianCalendar.is_leap_year(year)][month - 1]:
            raise ValueError("Day must be between 1 and number of days in month, while it is {}.".format(day))
        self._year = year
        self._month = month
        self._day = day

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    def to_rata_die(self):
        return (365 * (self._year - 1) + (self._year - 1) // 4 - (self._year - 1) // 100 + (self._year - 1) // 400
                + (367 * self._month - 362) // 12
                + ((-1 if GregorianCalendar.is_leap_year(self._year) else -2) if self._month > 2 else 0) + self._day)

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0) and (year % 400 not in (100, 200, 300))

    @classmethod
    def year_day(cls, year, day):
        if day < 1 or day > (366 if GregorianCalendar.is_leap_year(year) else 365):
            raise ValueError("Day must be between 1 and number of days in year, while it is {}.".format(day))
        month = bisect.bisect_left(_days_in_previous_months[GregorianCalendar.is_leap_year(year)], day)
        day_in_month = day - _days_in_previous_months[GregorianCalendar.is_leap_year(year)][month - 1]
        return cls(year, month, day_in_month)

    @classmethod
    def from_rata_die(cls, day_count):
        y400, d400 = divmod(day_count - 1, 146097)
        y100, d100 = divmod(d400, 36524)
        y4, d4 = divmod(d100, 1461)
        y1 = d4 // 365
        year_minus_one = 400 * y400 + 100 * y100 + 4 * y4 + y1 - (1 if (y100 == 4 or y1 == 4) else 0)
        days = day_count - 365 * year_minus_one - year_minus_one // 4 + year_minus_one // 100 - year_minus_one // 400      # days from january 1st (included) to today
        return cls.year_day(year_minus_one + 1, days)
