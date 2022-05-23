# datetime2 package main file

# Copyright (c) 2011-2022 Francesco Ricciardi
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


import time
from fractions import Fraction
from math import floor

from .common import verify_fractional_value, verify_fractional_value_num_den
from . import western, modern


##############################################################################
# OS dependent functions
#
def get_moment_complete():
    """Return local date and time as day_count, local time as day fraction, and,
    if possible, distance from UTC as fraction of a day."""
    try:
        moment_ns = (time.time_ns())  # time in ns from epoch; note epoch is platform dependent
    except AttributeError:
        moment_ns = int(time.time() * 1_000_000_000)  # time() returns a float in second
    # for the moment we are using time module's functions to get localtime
    # TODO: check if possible to implement something independent from time module, see e.g. tzlocal
    seconds, nanoseconds = divmod(moment_ns, 1_000_000_000)
    moment = time.localtime(seconds)
    year = moment.tm_year
    days_before_year = ((year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400)
    day_count = days_before_year + moment.tm_yday
    day_frac = (Fraction(moment.tm_hour, 24)   + Fraction(moment.tm_min, 1440) +
                Fraction(moment.tm_sec, 86400) + Fraction(nanoseconds, 86_400_000_000_000))
    utcoffset = Fraction(moment.tm_gmtoff, 86400)
    return day_count, day_frac, utcoffset


##############################################################################
#
# TimeDelta
#
##############################################################################


class TimeDelta:
    # ==>> STUB <<==
    def __init__(self, days):
        self._days = Fraction(days)

    def __repr__(self):
        return f"TimeDelta({self.days})"

    def __eq__(self, other):
        return self._days == other._days

    @property
    def days(self):
        return self._days


##############################################################################
#
# Date
#
##############################################################################


class Date:
    def __init__(self, day_count):
        # TODO: consider using the number hierarchy
        if isinstance(day_count, int):
            self._day_count = day_count
        else:
            raise TypeError("day_count argument for Date must be an integer.")

    @classmethod
    def today(cls):
        return cls(get_moment_complete()[0])

    @property
    def day_count(self):
        return self._day_count

    def __repr__(self):
        return f"datetime2.{type(self).__name__}({self.day_count})"

    def __str__(self):
        return f"R.D. {self.day_count}"

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            if other.days != floor(other.days):
                raise ValueError("Date object cannot be added to non integral TimeDelta.")
            return type(self)(self.day_count + floor(other.days))  # this way we ensure day count is integer
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Date):
            return TimeDelta(self.day_count - other.day_count)
        elif isinstance(other, TimeDelta):
            if other.days != floor(other.days):
                raise ValueError("Non integral TimeDelta cannot be subtracted from Date.")
            return type(self)(self.day_count - floor(other.days))
        else:
            return NotImplemented

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, Date):
            return self.day_count == other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Date):
            return self.day_count != other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            return True

    def __gt__(self, other):
        if isinstance(other, Date):
            return self.day_count > other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __ge__(self, other):
        if isinstance(other, Date):
            return self.day_count >= other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __le__(self, other):
        if isinstance(other, Date):
            return self.day_count <= other.day_count
        elif hasattr(other, "day_count"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    # hash value
    def __hash__(self):
        return hash(self._day_count)

    @classmethod
    def register_new_calendar(cls, attribute_name, calendar_class):
        if not isinstance(attribute_name, str) or not attribute_name.isidentifier():
            raise ValueError(f"Invalid calendar attribute name: {attribute_name}.")
        if hasattr(cls, attribute_name):
            raise AttributeError(f"Calendar attribute already existing: {attribute_name}.")
        if not hasattr(calendar_class, "from_rata_die"):
            raise TypeError("Calendar class does not have method from_rata_die.")
        if not hasattr(calendar_class, "to_rata_die"):
            raise TypeError("Calendar class does not have method to_rata_die.")

        class ModifiedClass(type):
            def __call__(klass, *args, **kwargs):
                calendar_obj = super().__call__(*args, **kwargs)
                date_obj = cls(calendar_obj.to_rata_die())
                setattr(date_obj, attribute_name, calendar_obj)
                return date_obj

        # Create the modified calendar class
        new_class_name = f"{calendar_class.__name__}In{cls.__name__}"
        modified_calendar_class = ModifiedClass(new_class_name, (calendar_class,), {})

        class CalendarAttribute:
            # This class implements a context dependent attribute
            def __init__(self, attribute_name, modified_calendar_class):
                self.attribute_name = attribute_name
                self.modified_calendar_class = modified_calendar_class

            def __get__(self, instance, owner):
                if instance is None:
                    return self.modified_calendar_class
                else:
                    assert self.attribute_name not in instance.__dict__
                    date_obj = self.modified_calendar_class.from_rata_die(instance.day_count)
                    calendar_obj = getattr(date_obj, self.attribute_name)
                    setattr(instance, self.attribute_name, calendar_obj)
                    return calendar_obj

        setattr(cls, attribute_name, CalendarAttribute(attribute_name, modified_calendar_class))


##############################################################################
# Register current calendars
#
Date.register_new_calendar("gregorian", western.GregorianCalendar)
Date.register_new_calendar("iso", modern.IsoCalendar)


##############################################################################
#
# Time
#
##############################################################################


class Time:
    def __init__(self, numerator, denominator=None, *, utcoffset=None):
        if denominator is None:
            self._day_frac = verify_fractional_value(numerator, min=0, max_excl=1)
        else:
            self._day_frac = verify_fractional_value_num_den(numerator, denominator, min=0, max_excl=1)
        if utcoffset is None:
            # naive instance
            self._utcoffset = None
        else:
            # aware instance
            self._utcoffset = verify_fractional_value(utcoffset, min=-1, max=1)

    @classmethod
    def now(cls, utcoffset=None):
        current_moment = get_moment_complete()
        if utcoffset is None:
            return cls(current_moment[1], utcoffset=current_moment[2])
        else:
            valid_utcoffset = verify_fractional_value(utcoffset, min=-1, max=1)
            delta = current_moment[2] - valid_utcoffset
            day_frac_temp = current_moment[1] - delta + 2  # +2 needed to avoid underruns
            new_day_frac = day_frac_temp - int(day_frac_temp)  # as so we eliminate the +2 above
            return cls(new_day_frac, utcoffset=valid_utcoffset)

    @classmethod
    def localnow(cls):
        current_moment = get_moment_complete()
        return cls(current_moment[1])

    @classmethod
    def utcnow(cls):
        current_moment = get_moment_complete()
        utcnow = current_moment[1] - current_moment[2]
        if utcnow < 0:
            utcnow += 1
        elif utcnow >= 1:
            utcnow -= 1
        return cls(utcnow)

    @property
    def day_frac(self):
        return self._day_frac

    @property
    def utcoffset(self):
        return self._utcoffset

    def __repr__(self):
        if self.utcoffset is None:
            return f"datetime2.{type(self).__name__}('{self.day_frac!s}')"
        else:
            return f"datetime2.{type(self).__name__}('{self.day_frac!s}', utcoffset='{self.utcoffset!s}')"

    def __str__(self):
        if self.utcoffset is None:
            return f"{self.day_frac!s} of a day"
        else:
            return f"{self.day_frac!s} of a day, {self.utcoffset!s} of a day from UTC"

    # Math operators
    def __add__(self, other):
        if isinstance(other, TimeDelta):
            total = self.day_frac + other.days
            return type(self)(total - floor(total), utcoffset=self.utcoffset)
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Time):
            if self.utcoffset:
                if other.utcoffset is None:
                    raise ValueError("You cannot mix naive and aware instances.")
                self_utc = self.day_frac - self.utcoffset
                other_utc = other.day_frac -  other.utcoffset
                delta = self_utc - other_utc
            else:
                if other.utcoffset is not None:
                    raise ValueError("You cannot mix naive and aware instances.")
                delta = self.day_frac - other.day_frac
            if delta <= Fraction(-1, 2):
                delta += 1
                while delta <= Fraction(-1, 2):
                    delta += 1
            elif delta > Fraction(1, 2):
                delta -= 1
                while delta > Fraction(1, 2):
                    delta -= 1
            return TimeDelta(delta)
        elif isinstance(other, TimeDelta):
            total = self.day_frac - other.days
            return type(self)(total - floor(total), utcoffset=self.utcoffset)
        else:
            return NotImplemented

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac == other.day_frac
                else:
                    return False
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset == other.day_frac - other.utcoffset
                else:
                    return False
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac != other.day_frac
                else:
                    return True
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset != other.day_frac - other.utcoffset
                else:
                    return True
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            return True

    def __gt__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac > other.day_frac
                else:
                    raise TypeError("You cannot compare a naive Time instance with an aware one.")
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset > other.day_frac - other.utcoffset
                else:
                    raise TypeError("You cannot compare an aware Time instance with a naive one.")
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __ge__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac >= other.day_frac
                else:
                    raise TypeError("You cannot compare a naive Time instance with an aware one.")
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset >= other.day_frac - other.utcoffset
                else:
                    raise TypeError("You cannot compare an aware Time instance with a naive one.")
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __lt__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac < other.day_frac
                else:
                    raise TypeError("You cannot compare a naive Time instance with an aware one.")
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset < other.day_frac - other.utcoffset
                else:
                    raise TypeError("You cannot compare an aware Time instance with a naive one.")
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    def __le__(self, other):
        if isinstance(other, Time):
            if self.utcoffset is None:
                if other.utcoffset is None:
                    return self.day_frac <= other.day_frac
                else:
                    raise TypeError("You cannot compare a naive Time instance with an aware one.")
            else:
                if other.utcoffset is not None:
                    return self.day_frac - self.utcoffset <= other.day_frac - other.utcoffset
                else:
                    raise TypeError("You cannot compare an aware Time instance with a naive one.")
        elif hasattr(other, "day_frac") and hasattr(other, "utcoffset"):
            return NotImplemented
        else:
            raise TypeError(f"You cannot compare '{type(self)!s}' with '{type(other)!s}'.")

    # hash value
    def __hash__(self):
        if self.utcoffset is None:
            return hash((self.day_frac, None))
        else:
            return hash(self.day_frac - self.utcoffset)

    @classmethod
    def register_new_time(cls, attribute_name, time_repr_class):
        if not isinstance(attribute_name, str) or not attribute_name.isidentifier():
            raise ValueError(f"Invalid attribute name ('{attribute_name}') for time representation.")
        if hasattr(cls, attribute_name):
            raise AttributeError(f"Time representation attribute already existing: {attribute_name}.")
        if not hasattr(time_repr_class, "from_time_pair"):
            raise TypeError("Time representation class does not have method from_time_pair.")
        if not hasattr(time_repr_class, "to_time_pair"):
            raise TypeError("Time representation class does not have method to_time_pair.")

        class ModifiedClass(type):
            def __call__(klass, *args, **kwargs):
                time_repr_obj = super().__call__(*args, **kwargs)
                day_frac, utcoffset = time_repr_obj.to_time_pair()
                time_obj = cls(day_frac, utcoffset=utcoffset)
                setattr(time_obj, attribute_name, time_repr_obj)
                return time_obj

        # Create the modified calendar class
        new_class_name = f"{time_repr_class.__name__}In{cls.__name__}"
        modified_time_repr_class = ModifiedClass(new_class_name, (time_repr_class,), {})

        class TimeReprAttribute:
            # This class implements a context dependent attribute
            def __init__(self, attr_name, modified_time_repr_class):
                self.attr_name = attr_name
                self.modified_time_repr_class = modified_time_repr_class

            def __get__(self, instance, owner):
                if instance is None:
                    return self.modified_time_repr_class
                else:
                    assert self.attr_name not in instance.__dict__
                    time_obj = self.modified_time_repr_class.from_time_pair(instance.day_frac, utcoffset=instance.utcoffset)
                    time_repr_obj = getattr(time_obj, self.attr_name)
                    setattr(instance, self.attr_name, time_repr_obj)
                    return time_repr_obj

        setattr(cls, attribute_name, TimeReprAttribute(attribute_name, modified_time_repr_class))


##############################################################################
# Register current time representations
#
Time.register_new_time("western", western.WesternTime)
Time.register_new_time("internet", modern.InternetTime)
