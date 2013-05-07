# datetime2 package main file

# Copyright (c) 2011-2012 Francesco Ricciardi
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
from calendars import gregorian


##############################################################################
# OS dependent functions
#
def get_moment():
    "Return date and time as day_count and day fraction."
    moment = time.localtime()
    year = moment.tm_year
    days_before_year = (year - 1) * 365 + (year - 1) // 4 - (year - 1) // 100 + (year - 1) // 400
    day_frac = Fraction(moment.tm_hour, 24) + Fraction(moment.tm_min, 1440) + Fraction(moment.tm_sec, 86400)
    return days_before_year + moment.tm_yday + day_frac


##############################################################################
# Core classes
#

class TimeDelta:
    #==>> STUB <<==
    def __init__(self, days):
        self._days = days
        
    def __repr__(self):
        return "TimeDelta({})".format(self.days)
    
    @property
    def days(self):
        return self._days
    
    def __add__(self, other):
        raise TypeError   # required to let Date tests pass

class Date:
    def __init__(self, day_count):
        if isinstance(day_count, int):
            self._day_count = day_count
        else:
            try:
                rata_die = day_count.to_rata_die()
            except AttributeError:
                raise TypeError("an integer or an object with the to_rata_die method is required")
            if isinstance(rata_die, int):
                self._day_count = rata_die
            else:
                raise TypeError("the to_rata_die method of {} does not return an integer.".format(str(day_count)))

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
            return Date(self.day_count + other.days)
        else:
            return NotImplemented
        
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, Date):
            return TimeDelta(self.day_count - other.day_count)
        elif isinstance(other, TimeDelta):
            return Date(self.day_count - other.days)
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
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Date):
            return self.day_count >= other.day_count
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, Date):
            return self.day_count <= other.day_count
        else:
            return NotImplemented

    # hash value
    def __hash__(self):
        return hash(self._day_count)


##############################################################################
# Support functions and classes
# This probably will be moved to a class which will be mixed in Date
    def register_new_calendar(self, calendar_attribute, calendar_class, constructors=(), special_methods=()):
        class CalendarAttribute:
            # This class will implement a context dependent attribute
            def __init__(self, attribute_name, calendar_class):
                self.attribute_name = attribute_name
                self.calendar_class = calendar_class

            def __get__(self, instance, owner):
                if instance is None:
                    return self.calendar_class
                else:
                    try:
                        calendar_obj = instance.__dict__[self.attribute_name]
                        return calendar_obj
                    except KeyError:
                        try:

                        calendar_obj = self.interface_class.from_rata_die(owner.day_count)
                        owner.calendars[self.attribute_name] = calendar_obj
                        return calendar_obj


        def new_get(self, obj, objtype):
            if obj is None:
                return GregorianCalendarToDateFactory   #######
            else:
                try:
                    return self.__dict__[gregorian]
                except KeyError:
                    greg_obj = gregorian.GregorianCalendar.from_rata_die(obj.day_count)
                    obj.gregorian = greg_obj
                    return greg_obj

##############################################################################
# Calendar registrations
#
Date.gregorian = GregorianInDateAttribute()
# stub to verify test code
# Date.iso = GregorianInDateAttribute()


def _create_date_factory(calendar_class, attribute_name, class_methods, static_methods):
    new_class_name = '{}Factory'.format(calendar_class.__name__)
    def new_method(self, *args, **kwargs):
        cal_obj = calendar_class(*args, **kwargs)
        date_obj = Date(cal_obj.to_rata_die())
        dummy1 = date_obj.__dict__
        dummy3 = Date.gregorian
        dummy2 = date_obj.gregorian
        setattr(date_obj, attribute_name, cal_obj)
        return date_obj
    new_methods = {'__new__': new_method}
    for name in static_methods:
        current_method = getattr(calendar_class, name)
        new_methods[name] = staticmethod(current_method)
    for name in class_methods:
        def new_class_method(cls, *args, **kwargs):
            cal_obj = getattr(calendar_class, name)(*args, **kwargs)
            date_obj = Date(cal_obj.to_rata_die())
            setattr(date_obj, attribute_name, cal_obj)
            return date_obj
        new_methods[name] = classmethod(new_class_method)
    return type(new_class_name, (), new_methods)

GregorianCalendarToDateFactory = _create_date_factory(gregorian.GregorianCalendar, 'gregorian', ('year_day',), ('days_in_year', 'is_leap_year'))

class GregorianInDateAttribute:
    def __get__(self, obj, objtype):
        if obj is None:
            return GregorianCalendarToDateFactory
        else:
            try:
                dummy = self.__dict__[gregorian]
                return dummy
            except KeyError:
                greg_obj = gregorian.GregorianCalendar.from_rata_die(obj.day_count)
                obj.gregorian = greg_obj
                return greg_obj



