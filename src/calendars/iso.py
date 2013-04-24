# ISO calendar in calendars package

# Copyright (c) 2013 Francesco Ricciardi
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


__all__ = ['IsoCalendar']


import bisect


_long_years = frozenset([  4,   9,  15,  20,  26,  32,  37,  43,  48,
                          54,  60,  65,  71,  76,  82,  88,  93,  99,
                         105, 111, 116, 122, 128, 133, 139, 144,
                         150, 156, 161, 167, 172, 178, 184, 189, 195,
                         201, 207, 212, 218, 224, 229, 235, 240, 246,
                         252, 257, 263, 268, 274, 280, 285, 291, 296,
                         303, 308, 314, 320, 325, 331, 336, 342, 348,
                         353, 359, 364, 370, 376, 381, 387, 392, 398])

_weeks_in_previous_years = [ 0 ]
for year_index in range(1, 400):
    _weeks_in_previous_years.append(_weeks_in_previous_years[-1] + (52 if year_index not in _long_years else 53))

# This code pretty prints the week-in-previous-years list
#for row in range (20):
#    print('{:3d}: {}'.format(row * 20, " ".join(['{:5d}'.format(_weeks_in_previous_years[y + row * 20]) for y in range(20)])))

##############################################################################
# Iso calendar
#
class IsoCalendar:
    def __init__(self, year, week, day):
        if not isinstance(year, int) or not isinstance(week, int) or not isinstance(day, int):
            raise TypeError("integer argument expected")
        if week < 1 or week > IsoCalendar.weeks_in_year(year):
            raise ValueError("Week must be between 1 and number of weeks in year, while it is {}.".format(week))
        if day < 1 or day > 7:
            raise ValueError("Day must be between 1 and 7, while it is {}.".format(day))
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
        week_no_less_1, day_less_1 = divmod(day_count - 1, 7)                           # ranges: week_no_less_1: free, day_less_1: 0..6
        four_hundred_years, no_of_weeks_in_400 = divmod(week_no_less_1, 20871)          # ranges: four_hundred_years: free, no_of_weeks_in_400: 0..20870
        year_in_400 = bisect.bisect_right(_weeks_in_previous_years, no_of_weeks_in_400) # range: year_in_400: 1..400
        year = year_in_400 + four_hundred_years * 400
        week = no_of_weeks_in_400 - _weeks_in_previous_years[year_in_400 - 1] + 1
        day = day_less_1 + 1
        #print(day_count, week_no_less_1, day_less_1, four_hundred_years, no_of_weeks_in_400, year_in_400, year, week, day)
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
            self._rata_die = y400 * 146097 + 7 * (_weeks_in_previous_years[year_in_400] + self.week - 1) + self.day
        return self._rata_die

    def day_of_year(self):
        return 7 * (self.week - 1) + self.day

    def replace(self, *, year = None, week = None, day = None):
        if year is None:
            year = self.year
        if week is None:
            week = self.week
        if day is None:
            day = self.day
        return IsoCalendar(year, week, day)

    # Comparison operators
    def __eq__(self, other):
        return isinstance(other, IsoCalendar) and self.year == other.year and self.week == other.week and self.day == other.day

    def __ne__(self, other):
        return not isinstance(other, IsoCalendar) or self.day != other.day or self.week != other.week or self.year != other.year

    def __gt__(self, other):
        if isinstance(other, IsoCalendar):
            return (self.year, self.week, self.day) > (other.year, other.week, other.day)
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, IsoCalendar):
            return (self.year, self.week, self.day) >= (other.year, other.week, other.day)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, IsoCalendar):
            return (self.year, self.week, self.day) < (other.year, other.week, other.day)
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, IsoCalendar):
            return (self.year, self.week, self.day) <= (other.year, other.week, other.day)
        else:
            return NotImplemented

    # hash value
    def __hash__(self):
        return hash((self.year, self.week, self.day))

    def __repr__(self):
        return 'calendars.iso.{}({}, {}, {})'.format(self.__class__.__name__, self.year, self.week, self.day)

    def __str__(self):
        if self.year >= 0:
            return '{:04d}-W{:02d}-{:02d}'.format(self.year, self.week, self.day)
        else:
            return '{:05d}-W{:02d}-{:02d}'.format(self.year, self.week, self.day)