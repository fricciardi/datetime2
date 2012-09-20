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


from math import floor
from functools import total_ordering

from . import osinterface
from .calendars import gregorian


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

@total_ordering
class Date:
    def __init__(self, day_count):
        if isinstance(day_count, int):
            self._day_count = day_count
        else:
            raise TypeError("an integer is required")

    @classmethod
    def today(cls):
        return cls(floor(osinterface.get_moment()))

    @property
    def day_count(self):
        return self._day_count
    
    def __repr__(self):
        return "Date({})".format(self.day_count)
    
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
        
    # TODO: undestand if we want to use total ordering
    def __eq__(self, other):
        return isinstance(other, Date) and self.day_count == other.day_count

    def __lt__(self, other):
        if isinstance(other, Date):
            return self.day_count < other.day_count
        else:
            return NotImplemented
        
    def __hash__(self):
        return hash(self._day_count)


##############################################################################
# Support functions and classes
#
def _create_calendar_to_date(class_to_convert, instance_modifiers):
    new_class_name = '{}ToDate'.format(class_to_convert.__name__)
    new_constructors = {}
    for name in instance_modifiers:
        current_method = getattr(class_to_convert, name)
        def new_method(self, *args, **kwargs):
            calendar_obj = current_method(self, *args, **kwargs)
            return Date(calendar_obj.to_rata_die())
        new_method_name = '{}_to_date'.format(name)
        new_constructors[new_method_name] = new_method
    return type(new_class_name, (class_to_convert,), new_constructors)

GregorianCalendarToDate = _create_calendar_to_date(gregorian.GregorianCalendar, ('replace',))

def _create_date_factory(calendar_class, attribute_name, class_methods, static_methods):
    new_class_name = '{}Factory'.format(calendar_class.__name__)
    def new_method(self, *args, **kwargs):
        cal_obj = calendar_class(*args, **kwargs)
        date_obj = Date(cal_obj.to_rata_die())
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

GregorianCalendarToDateFactory = _create_date_factory(GregorianCalendarToDate, 'gregorian', ('year_day',), ('days_in_year', 'is_leap_year'))

class GregorianInDateAttribute:
    def __get__(self, obj, objtype):
        if obj is None:
            return GregorianCalendarToDateFactory
        else:
            try:
                return self.__dict__[gregorian]
            except KeyError:
                greg_obj = GregorianCalendarToDate.from_rata_die(obj.day_count)
                obj.gregorian = greg_obj
                return greg_obj


class CalendarInDateAttribute:
    # This class will implement a context dependent attribute
    def __init__(self, attribute_name, interface_class):
        self.attribute_name = attribute_name
        self.interface_class = interface_class

    def __get__(self, instance, owner):
        if instance is None:
            calendar_obj = self.interface_class.from_rata_die(owner.day_count)
            return self.interface_class
        else:
            try:
                return owner.calendars[self.attribute_name]
            except KeyError:
                calendar_obj = self.interface_class.from_rata_die(owner.day_count)
                owner.calendars[self.attribute_name] = calendar_obj
                return calendar_obj


##############################################################################
# Calendar registration
#
Date.gregorian = GregorianInDateAttribute()
# stub to verify test code
Date.iso = GregorianInDateAttribute()

