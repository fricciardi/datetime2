# datetime2 package main file

# Copyright (c) 2011-2019 Francesco Ricciardi
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

import time
from fractions import Fraction
from math import floor
from functools import total_ordering

from datetime2 import western, modern




##############################################################################
# OS dependent functions
#
def get_moment():
    """Return date and time as day_count and day fraction."""
    # TODO: check if it possible to have greater resolution
    moment = time.localtime()
    year = moment.tm_year
    days_before_year = (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    day_frac = Fraction(moment.tm_hour, 24) + Fraction(moment.tm_min, 1440) + Fraction(moment.tm_sec, 86400)
    return days_before_year + moment.tm_yday + day_frac


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
        return "TimeDelta({})".format(self.days)

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
            raise TypeError("day_count argument for Date must be an integer.".format(str(day_count)))

    @classmethod
    def today(cls):
        return cls(floor(get_moment()))

    @property
    def day_count(self):
        return self._day_count
    
    def __repr__(self):
        return "datetime2.{}({})".format(self.__class__.__name__, self.day_count)
    
    def __str__(self):
        return "R.D. {}".format(self.day_count)
    
    def __add__(self, other):
        if isinstance(other, TimeDelta):
            if other.days != floor(other.days):
                raise ValueError("Date object cannot be added to non integral TimeDelta.")
            return Date(self.day_count + floor(other.days)) # this way we ensure day count is integer
        else:
            return NotImplemented
        
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Date):
            return TimeDelta(self.day_count - other.day_count)
        elif isinstance(other, TimeDelta):
            if other.days != floor(other.days):
                raise ValueError("non integral TimeDelta cannot be subtracted from Date.")
            return Date(self.day_count - floor(other.days))
        else:
            return NotImplemented

    # Comparison operators
    def __eq__(self, other):
        return isinstance(other, Date) and self.day_count == other.day_count

    def __ne__(self, other):
        return not isinstance(other, Date) or self.day_count != other.day_count

    def __gt__(self, other):
        if isinstance(other, Date):
            return self.day_count > other.day_count
        elif hasattr(other, 'day_count'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __ge__(self, other):
        if isinstance(other, Date):
            return self.day_count >= other.day_count
        elif hasattr(other, 'day_count'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        elif hasattr(other, 'day_count'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __le__(self, other):
        if isinstance(other, Date):
            return self.day_count <= other.day_count
        elif hasattr(other, 'day_count'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    # hash value
    def __hash__(self):
        return hash(self._day_count)

    @classmethod
    def register_new_calendar(cls, attribute_name, calendar_class):
        if not isinstance(attribute_name, str) or not attribute_name.isidentifier():
            raise ValueError('Invalid calendar attribute name: {}.'.format(attribute_name))
        if hasattr(cls, attribute_name):
            raise AttributeError('Calendar attribute already existing: {}.'.format(attribute_name))
        if not hasattr(calendar_class, 'from_rata_die'):
            raise TypeError('Calendar class does not have method from_rata_die.')
        if not hasattr(calendar_class, 'to_rata_die'):
            raise TypeError('Calendar class does not have method to_rata_die.')

        class ModifiedClass(type):
            def __call__(klass, *args, **kwargs):
                calendar_obj = super().__call__(*args, **kwargs)
                date_obj = cls(calendar_obj.to_rata_die())
                setattr(date_obj, attribute_name, calendar_obj)
                return date_obj

        # Create the modified calendar class
        new_class_name = '{}In{}'.format(calendar_class.__name__, cls.__name__)
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
Date.register_new_calendar('gregorian', western.GregorianCalendar)
Date.register_new_calendar('iso', modern.IsoCalendar)


##############################################################################
#
# Time
#
##############################################################################

class Time:
    def __init__(self, day_frac, *, correction=None):
        self.correction = correction  # for the time being
        try:
            if type(day_frac) == tuple:
                if len(day_frac) == 2:
                    self._day_frac = Fraction(*day_frac)
                else:
                    raise TypeError('Time argument tuple is invalid')
            else:
                self._day_frac = Fraction(day_frac)
        except ZeroDivisionError:
            raise ZeroDivisionError("Time denominator cannot be zero.".format(str(day_frac)))
        if self.day_frac < 0 or self.day_frac >= 1:
            raise ValueError("resulting fraction is outside range valid for Time instances (0 <= value < 1): {}".format(float(self.day_frac)))

    @classmethod
    def now(cls):
        current_moment = get_moment()
        return cls(current_moment - floor(current_moment))

    @property
    def day_frac(self):
        return self._day_frac

    def __repr__(self):
        return "datetime2.{}('{}')".format(self.__class__.__name__, str(self.day_frac))

    def __str__(self):
        return "{} of a day".format(str(self.day_frac))

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            total = self.day_frac + other.days
            return Time(total - floor(total))
        else:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Time):
            return TimeDelta(self.day_frac - other.day_frac)
        elif isinstance(other, TimeDelta):
            total = self.day_frac - other.days
            return Time(total - floor(total))
        else:
            return NotImplemented

    # Comparison operators
    def __eq__(self, other):
        return isinstance(other, Time) and self.day_frac == other.day_frac

    def __ne__(self, other):
        return not isinstance(other, Time) or self.day_frac != other.day_frac

    def __gt__(self, other):
        if isinstance(other, Time):
            return self.day_frac > other.day_frac
        elif hasattr(other, 'day_frac'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __ge__(self, other):
        if isinstance(other, Time):
            return self.day_frac >= other.day_frac
        elif hasattr(other, 'day_frac'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __lt__(self, other):
        if isinstance(other, Time):
            return self.day_frac < other.day_frac
        elif hasattr(other, 'day_frac'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    def __le__(self, other):
        if isinstance(other, Time):
            return self.day_frac <= other.day_frac
        elif hasattr(other, 'day_frac'):
            return NotImplemented
        else:
            raise TypeError("You cannot compare '{}' with '{}'.".format(str(type(self)), str(type(other))))

    # hash value
    def __hash__(self):
        return hash(self._day_frac)

    @classmethod
    def register_new_time(cls, attribute_name, time_repr_class):
        if not isinstance(attribute_name, str) or not attribute_name.isidentifier():
            raise ValueError("Invalid attribute name ('{}') for time representation.".format(attribute_name))
        if hasattr(cls, attribute_name):
            raise AttributeError('Time representation attribute already existing: {}.'.format(attribute_name))
        if not hasattr(time_repr_class, 'from_day_frac'):
            raise TypeError('Time representation class does not have method from_day_frac.')
        if not hasattr(time_repr_class, 'to_day_frac'):
            raise TypeError('Time representation class does not have method to_day_frac.')

        class ModifiedClass(type):
            def __call__(klass, *args, **kwargs):
                time_repr_obj = super().__call__(*args, **kwargs)
                time_obj = cls(time_repr_obj.to_day_frac())
                setattr(time_obj, attribute_name, time_repr_obj)
                return time_obj

        # Create the modified calendar class
        new_class_name = '{}In{}'.format(time_repr_class.__name__, cls.__name__)
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
                    time_obj = self.modified_time_repr_class.from_day_frac(instance.day_frac)
                    time_repr_obj = getattr(time_obj, self.attr_name)
                    setattr(instance, self.attr_name, time_repr_obj)
                    return time_repr_obj

        setattr(cls, attribute_name, TimeReprAttribute(attribute_name, modified_time_repr_class))


##############################################################################
# Register current time representations
#
Time.register_new_time('western', western.WesternTime)
Time.register_new_time('internet', modern.InternetTime)

